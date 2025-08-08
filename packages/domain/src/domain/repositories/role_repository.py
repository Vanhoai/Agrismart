from domain.entities import RoleEntity
from domain.repositories import IBaseRepository


class IRoleRepository(IBaseRepository[RoleEntity]):
    pass
