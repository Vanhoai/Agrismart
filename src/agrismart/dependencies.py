import os
from fastapi import Depends

from core.configuration import Configuration
from core.database import Database, CollectionName
from core.secures import Cryptography, KeyBackend, Jwt

from domain.repositories import AccountRepository, RoleRepository
from domain.services import AuthService, AccountService, RoleService, MediaService

from infrastructure.apis import Supabase, Cloudinary
from infrastructure.augmenters import Augmenter


def build_config() -> Configuration:
    return Configuration()


def build_cryptography() -> Cryptography:
    directory = os.path.join(os.getcwd(), "keys")
    cryptography = Cryptography(directory, KeyBackend.EC, is_override=False, is_caching=True)
    cryptography.generate()
    return cryptography


def build_jwt(cryptography: Cryptography = Depends(build_cryptography)):
    return Jwt(cryptography)


def build_supabase(config: Configuration = Depends(build_config)) -> Supabase:
    return Supabase(config)


def build_database(config: Configuration = Depends(build_config)) -> Database:
    return Database(config)


async def augmenter_monitor():
    config = build_config()
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


def build_auth_service(
        account_repository: AccountRepository = Depends(build_account_repository),
        supabase: Supabase = Depends(build_supabase),
        jwt: Jwt = Depends(build_jwt),
) -> AuthService:
    return AuthService(account_repository, supabase, jwt)


def build_account_service(
        account_repository: AccountRepository = Depends(build_account_repository),
) -> AccountService:
    return AccountService(account_repository)


def build_role_service(
        role_repository: RoleRepository = Depends(build_role_repository),
        account_repository: AccountRepository = Depends(build_account_repository),
) -> RoleService:
    return RoleService(role_repository, account_repository)


def build_media_service() -> MediaService:
    return MediaService()
