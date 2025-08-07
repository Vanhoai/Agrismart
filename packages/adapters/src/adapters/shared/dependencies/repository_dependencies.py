from fastapi import Depends
from core.database import Database, CollectionName


from domain.repositories import (
    IAccountRepository,
    IRoleRepository,
    IPostRepository,
    ISessionRepository,
    IProviderRepository,
)


from adapters.secondary import (
    AccountRepository,
    RoleRepository,
    PostRepository,
    SessionRepository,
    ProviderRepository,
)

from .shared_dependencies import build_database


def build_account_repository(
    database: Database = Depends(build_database),
) -> IAccountRepository:
    collection = database.get_collection(CollectionName.ACCOUNTS)
    return AccountRepository(collection)


def build_role_repository(database: Database = Depends(build_database)) -> IRoleRepository:
    collection = database.get_collection(CollectionName.ROLES)
    return RoleRepository(collection)


def build_post_repository(database: Database = Depends(build_database)) -> IPostRepository:
    collection = database.get_collection(CollectionName.POSTS)
    return PostRepository(collection)


def build_session_repository(
    database: Database = Depends(build_database),
) -> ISessionRepository:
    collection = database.get_collection(CollectionName.SESSIONS)
    return SessionRepository(collection)


def build_provider_repository(
    database: Database = Depends(build_database),
) -> IProviderRepository:
    collection = database.get_collection(CollectionName.PROVIDERS)
    return ProviderRepository(collection)
