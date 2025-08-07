from fastapi import Depends

from core.secures import Jwt
from core.configuration import Configuration
from domain.services import (
    AuthService,
    AccountService,
    RoleService,
    MediaService,
    PostService,
)

from domain.repositories import (
    IAccountRepository,
    IRoleRepository,
    IPostRepository,
    ISessionRepository,
    IProviderRepository,
)

from adapters.secondary import Supabase, RabbitMQConnection

from .repository_dependencies import (
    build_account_repository,
    build_role_repository,
    build_post_repository,
    build_session_repository,
    build_provider_repository,
)
from .shared_dependencies import (
    build_supabase,
    config_from_state,
    build_jwt,
    queue_from_state,
)


def build_auth_service(
    account_repository: IAccountRepository = Depends(build_account_repository),
    session_repository: ISessionRepository = Depends(build_session_repository),
    provider_repository: IProviderRepository = Depends(build_provider_repository),
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
