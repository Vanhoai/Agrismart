from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Tuple

from core.base import Meta
from domain.entities import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class IBaseRepository(Generic[T], ABC):
    @abstractmethod
    async def create(self, entity: T) -> T: ...

    @abstractmethod
    async def find_one(self, query: dict) -> Optional[T]: ...

    @abstractmethod
    async def update_one(self, entity: T) -> T: ...

    @abstractmethod
    async def delete_one(self, query: dict) -> bool: ...

    @abstractmethod
    async def delete_many(self, query: dict) -> int: ...

    @abstractmethod
    async def find(self, query: Optional[dict] = None) -> List[T]: ...

    @abstractmethod
    async def paginated(
        self,
        query: Optional[dict] = None,
        page: int = 1,
        page_size: int = 20,
        order: str = "asc",
        order_by: str = "created_at",
    ) -> Tuple[List[T], Meta]: ...
