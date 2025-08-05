import os
from fastapi import Depends, Request

from core.configuration import Configuration
from core.database import Database, CollectionName
from core.secures import Cryptography, Jwt

from domain.repositories import (
    AccountRepository,
    RoleRepository,
    PostRepository,
    DiagnosticRepository,
    SessionRepository,
    ProviderRepository,
)
from domain.services import AuthService, AccountService, RoleService, MediaService, DiagnosticService
from domain.services.post_service import PostService

from infrastructure.apis import Supabase
from infrastructure.augmenters import Augmenter
from infrastructure.queues import RabbitMQConnection
from infrastructure.repositories import DiagnosticRepositoryImpl


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


async def augmenter_monitor(config: Configuration):
    database = build_database(config)
    csv_directory = os.path.join(os.getcwd(), "datasets", "databases")
    augmenter = Augmenter(csv_directory, database)
    await augmenter.monitor()


def build_account_repository(
    database: Database = Depends(build_database),
) -> AccountRepository:
    collection = database.get_collection(CollectionName.ACCOUNTS)
    return AccountRepository(collection)


def build_role_repository(database: Database = Depends(build_database)) -> RoleRepository:
    collection = database.get_collection(CollectionName.ROLES)
    return RoleRepository(collection)


def build_post_repository(database: Database = Depends(build_database)) -> PostRepository:
    collection = database.get_collection(CollectionName.POSTS)
    return PostRepository(collection)


def build_diagnostic_repository(
    config: Configuration = Depends(config_from_state),
) -> DiagnosticRepository:
    return DiagnosticRepositoryImpl(config)


def build_session_repository(
    database: Database = Depends(build_database),
) -> SessionRepository:
    collection = database.get_collection(CollectionName.SESSIONS)
    return SessionRepository(collection)


def build_provider_repository(
    database: Database = Depends(build_database),
) -> ProviderRepository:
    collection = database.get_collection(CollectionName.PROVIDERS)
    return ProviderRepository(collection)


def build_auth_service(
    account_repository: AccountRepository = Depends(build_account_repository),
    session_repository: SessionRepository = Depends(build_session_repository),
    provider_repository: ProviderRepository = Depends(build_provider_repository),
    supabase: Supabase = Depends(build_supabase),
    jwt: Jwt = Depends(build_jwt),
    config: Configuration = Depends(config_from_state),
) -> AuthService:
    return AuthService(
        account_repository,
        session_repository,
        provider_repository,
        supabase,
        jwt,
        config,
    )


def build_account_service(
    account_repository: AccountRepository = Depends(build_account_repository),
    provider_repository: ProviderRepository = Depends(build_provider_repository),
    supabase: Supabase = Depends(build_supabase),
) -> AccountService:
    return AccountService(account_repository, provider_repository, supabase)


def build_role_service(
    role_repository: RoleRepository = Depends(build_role_repository),
    account_repository: AccountRepository = Depends(build_account_repository),
) -> RoleService:
    return RoleService(role_repository, account_repository)


def build_media_service() -> MediaService:
    return MediaService()


def build_post_service(
    post_repository: PostRepository = Depends(build_post_repository),
    account_repository: AccountRepository = Depends(build_account_repository),
    queue: RabbitMQConnection = Depends(queue_from_state),
) -> PostService:
    return PostService(post_repository, account_repository, queue)


def build_diagnostic_service(
    diagnostic_repository: DiagnosticRepository = Depends(build_diagnostic_repository),
):
    return DiagnosticService(diagnostic_repository)
