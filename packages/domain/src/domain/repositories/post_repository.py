from domain.entities import PostEntity
from domain.repositories import IBaseRepository


class IPostRepository(IBaseRepository[PostEntity]):
    pass
