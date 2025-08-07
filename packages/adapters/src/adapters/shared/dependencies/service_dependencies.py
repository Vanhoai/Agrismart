from fastapi import Depends

from core.configuration import Configuration
from core.secures import Jwt

from adapters.secondary import RabbitMQConnection
from adapters.secondary import Supabase

from domain.repositories import (
    IAccountRepository,
    IRoleRepository,
    IPostRepository,
    ISessionRepository,
    IProviderRepository,
)

from domain.services import (
    AuthService,
    AccountService,
    RoleService,
    MediaService,
    PostService,
)

from .shared_dependencies import (
    config_from_state,
    queue_from_state,
    build_supabase,
    build_jwt,
)

from .repository_dependencies import (
    build_account_repository,
    build_role_repository,
    build_post_repository,
    build_session_repository,
    build_provider_repository,
)


def build_auth_service(
    jwt: Jwt = Depends(build_jwt),
    supabase: Supabase = Depends(build_supabase),
    config: Configuration = Depends(config_from_state),
    account_repository: IAccountRepository = Depends(build_account_repository),
    session_repository: ISessionRepository = Depends(build_session_repository),
    provider_repository: IProviderRepository = Depends(build_provider_repository),
) -> AuthService:
    return AuthService(
        jwt,
        supabase,
        config,
        account_repository,
        session_repository,
        provider_repository,
    )


def build_account_service(
    account_repository: IAccountRepository = Depends(build_account_repository),
    provider_repository: IProviderRepository = Depends(build_provider_repository),
    supabase: Supabase = Depends(build_supabase),
) -> AccountService:
    return AccountService(account_repository, provider_repository, supabase)


def build_role_service(
    role_repository: IRoleRepository = Depends(build_role_repository),
    account_repository: IAccountRepository = Depends(build_account_repository),
) -> RoleService:
    return RoleService(role_repository, account_repository)


def build_media_service() -> MediaService:
    return MediaService()


def build_post_service(
    post_repository: IPostRepository = Depends(build_post_repository),
    account_repository: IAccountRepository = Depends(build_account_repository),
    queue: RabbitMQConnection = Depends(queue_from_state),
) -> PostService:
    return PostService(post_repository, account_repository, queue)
