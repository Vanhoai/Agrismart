import asyncio
from loguru import logger
from aio_pika import connect_robust, Message
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel, AbstractIncomingMessage

from .consumers import push_notification


class RabbitMQConnection:
    def __init__(self, uri: str):
        self.uri = uri
        self.connection: AbstractRobustConnection | None = None
        self.channel: AbstractRobustChannel | None = None

    async def _clear(self) -> None:
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()

        self.connection = None
        self.channel = None

    async def disconnect(self) -> None:
        await self._clear()
        logger.info("Disconnected from RabbitMQ successfully! 👋🏻 🐰")

    async def connect(self) -> None:
        try:
            self.connection = await connect_robust(self.uri)
            self.channel = await self.connection.channel(publisher_confirms=False)  # type: ignore

            logger.info("Connected to RabbitMQ successfully! 🐰")
        except Exception as exception:
            await self._clear()
            logger.error(f"Failed to connect to RabbitMQ: {exception} 😵🐰")

    def status(self) -> bool:
        if not self.connection or self.connection.is_closed:
            return False
        if not self.channel or self.channel.is_closed:
            return False

        return True

    async def send_messages(self, messages: dict, routing_key: str) -> None:
        if not self.status():
            logger.error("RabbitMQ connection is not established. Cannot send messages.")
            return

        if not self.channel:
            logger.error("Channel is not established. Cannot send messages.")
            return

        async with self.channel.transaction():
            for message in messages:
                message = Message(
                    body=message.encode(),
                    delivery_mode=2,  # make message persistent
                )

                await self.channel.default_exchange.publish(
                    message,
                    routing_key=routing_key,
                )


PARALLEL_TASKS = 10
NOTIFICATION_QUEUE = "agrismart.notifications"


async def start_consumer(queue_connection: RabbitMQConnection) -> asyncio.Task:
    async def _consume():
        connection = queue_connection.connection  # Reuse connection
        if not connection or connection.is_closed:
            return

        channel = await connection.channel()
        await channel.set_qos(prefetch_count=PARALLEL_TASKS)
        queue = await channel.declare_queue(NOTIFICATION_QUEUE, auto_delete=True)

        logger.info(f"Started consuming from {NOTIFICATION_QUEUE} 👀")
        await queue.consume(push_notification)

        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            await channel.close()
            raise

    return asyncio.create_task(_consume())
