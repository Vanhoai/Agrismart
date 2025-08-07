import os
from fastapi import Depends, Request

from core.configuration import Configuration
from core.database import Database
from core.secures import Cryptography, Jwt

from adapters.secondary import RabbitMQConnection, Supabase

# Global instances
# _config = Configuration()
# _cryptography = None
# _rabbitmq_connection = None

# @lru_cache()
# def build_config() -> Configuration:
#     global _config
#     if _config is None:
#         _config = Configuration()
#     return _config

# @lru_cache()
# def build_rabbitmq_connection() -> RabbitMQConnection:
#     global _rabbitmq_connection
#     if _rabbitmq_connection is None:
#         _rabbitmq_connection = RabbitMQConnection(config.RABBITMQ_BROKER_URL)
#     return _rabbitmq_connection

# @lru_cache()
# def build_cryptography() -> Cryptography:
#     global _cryptography
#     if _cryptography is None:
#         directory = os.path.join(os.getcwd(), "keys")
#         _cryptography = Cryptography(directory, KeyBackend.EC, is_override=False, is_caching=True)
#         _cryptography.generate()
#     return _cryptography


def config_from_state(request: Request) -> Configuration:
    return request.app.state.config


def queue_from_state(request: Request) -> RabbitMQConnection:
    return request.app.state.queue


def cryptography_from_state(request: Request) -> Cryptography:
    return request.app.state.cryptography


# def build_rabbitmq_connection() -> RabbitMQConnection:
#     return RabbitMQConnection(config.RABBITMQ_BROKER_URL)


# def build_cryptography() -> Cryptography:
#     directory = os.path.join(os.getcwd(), "keys")
#     cryptography = Cryptography(directory, KeyBackend.EC, is_override=False, is_caching=True)
#     cryptography.generate()
#     return cryptography


def build_jwt(cryptography: Cryptography = Depends(cryptography_from_state)):
    return Jwt(cryptography)


def build_supabase(
    config: Configuration = Depends(config_from_state),
) -> Supabase:
    return Supabase(config)


def build_database(
    config: Configuration = Depends(config_from_state),
) -> Database:
    return Database(config, config.IS_LOCAL)


# async def augmenter_monitor(config: Configuration):
#     database = build_database(config)
#     csv_directory = os.path.join(os.getcwd(), "datasets", "databases")
#     augmenter = Augmenter(csv_directory, database)
#     await augmenter.monitor()
