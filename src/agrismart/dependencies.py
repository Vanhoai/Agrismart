from fastapi import Depends

from core.configuration import Configuration
from core.database import Database, CollectionName

from domain.repositories import AccountRepository, RoleRepository
from domain.services import AuthService, AccountService

from infrastructure.apis import Supabase


def build_config() -> Configuration:
    return Configuration()


def build_supabase(config: Configuration = Depends(build_config)) -> Supabase:
    return Supabase(config)


def build_database(config: Configuration = Depends(build_config)) -> Database:
    return Database(config)


def build_account_repository(
    database: Database = Depends(build_database),
) -> AccountRepository:
    collection = database.get_collection(CollectionName.ACCOUNTS)
    return AccountRepository(collection)


def role_repository(database: Database = Depends(build_database)) -> RoleRepository:
    collection = database.get_collection(CollectionName.ROLES)
    return RoleRepository(collection)


def build_auth_service(
    account_repository: AccountRepository = Depends(build_account_repository),
    supabase: Supabase = Depends(build_supabase),
) -> AuthService:
    return AuthService(account_repository, supabase)


def build_account_service(
    account_repository: AccountRepository = Depends(build_account_repository),
) -> AccountService:
    return AccountService(account_repository)
