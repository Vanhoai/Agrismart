import asyncio
from tabulate import tabulate
from typing import List, Callable
from loguru import logger
from aio_pika import connect_robust, Message
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel

from .consumers import notification_consumer, submission_consumer

PARALLEL_TASKS = 10

QUEUE_CONFIG = {
    "notifications": {
        "name": "agrismart.notifications",
        "handler": notification_consumer,
        "auto_delete": True,
    },
    "submissions": {
        "name": "agrismart.submissions",
        "handler": submission_consumer,
        "auto_delete": True,
    },
}


class RabbitMQConnection:
    def __init__(self, uri: str):
        self.uri = uri
        self.connection: AbstractRobustConnection | None = None
        self.channel: AbstractRobustChannel | None = None
        self.consumer_tasks: List[asyncio.Task] = []

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

    async def start_consumer(self, queue_name: str, handler: Callable, auto_delete: bool) -> asyncio.Task:
        async def _consume():
            if not self.connection or self.connection.is_closed:
                return

            channel = await self.connection.channel()
            await channel.set_qos(prefetch_count=PARALLEL_TASKS)
            queue = await channel.declare_queue(queue_name, auto_delete=auto_delete)

            logger.info(f"Started consuming from {queue_name} 👀")
            await queue.consume(handler)

            try:
                await asyncio.Future()
            except asyncio.CancelledError:
                await channel.close()
                logger.info(f"Stopped consuming from {queue_name} 👋🏻")
                raise

        return asyncio.create_task(_consume())

    async def start_all_consumers(self) -> List[asyncio.Task]:
        consumer_tasks = []

        for queue_config in QUEUE_CONFIG.values():
            if queue_config["handler"]:
                task = await self.start_consumer(
                    queue_config["name"],
                    queue_config["handler"],
                    queue_config["auto_delete"],
                )

                consumer_tasks.append(task)

        table = []
        for queue_name, config in QUEUE_CONFIG.items():
            row = [queue_name, config["handler"].__name__, config["auto_delete"]]
            table.append(row)

        print(
            tabulate(
                table,
                headers=["Queue Name", "Handler", "Auto Delete"],
                tablefmt="pretty",
            )
        )

        self.consumer_tasks = consumer_tasks
        return consumer_tasks

    async def stop_all_consumers(self):
        for task in self.consumer_tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        self.consumer_tasks.clear()
