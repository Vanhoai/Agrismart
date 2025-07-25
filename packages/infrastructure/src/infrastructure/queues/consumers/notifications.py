import json
from loguru import logger
from aio_pika.abc import AbstractIncomingMessage


async def notification_consumer(message: AbstractIncomingMessage):
    async with message.process():
        try:
            body = json.loads(message.body.decode())
            logger.info(f"Processing notification: {body}")
            # Your notification logic here
        except Exception as e:
            logger.error(f"Error processing notification: {e}")
