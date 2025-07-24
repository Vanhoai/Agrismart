from aio_pika.abc import AbstractIncomingMessage


async def push_notification(message: AbstractIncomingMessage):
    print(f"Pushing notification: {message}")
