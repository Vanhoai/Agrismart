from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List


# ============================= DOMAIN LAYER =============================
class BaseEntity:
    uuid: str
    created_at: str
    updated_at: str

    def __init__(self, uuid: str, created_at: str, updated_at: str) -> None:
        self.uuid = uuid
        self.created_at = created_at
        self.updated_at = updated_at


class AccountEntity(BaseEntity):
    email: str
    name: str
    age: int

    def __init__(self, uuid: str, email: str, name: str, age: int, created_at: str, updated_at: str) -> None:
        super().__init__(uuid, created_at, updated_at)
        self.email = email
        self.name = name
        self.age = age

    @staticmethod
    def fake_find_one() -> "AccountEntity":
        return AccountEntity(
            uuid="Ox1234567890abcdef12345678",
            email="vanhoai.adv@gmail.com",
            name="Hinsun",
            age=20,
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
        )

    @staticmethod
    def fake_create() -> "AccountEntity":
        return AccountEntity(
            uuid="Ox1234567890abcdef12345678",
            email="hinsun@gmail.com",
            name="Hinsun",
            age=25,
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
        )


T = TypeVar("T", bound=BaseEntity)


class IBaseRepository(Generic[T], ABC):
    @abstractmethod
    def create(self, entity: T) -> T: ...

    @abstractmethod
    def find_one(self, query: dict) -> Optional[T]: ...

    @abstractmethod
    def find_all(self) -> List[T]: ...

    @abstractmethod
    def update(self, uuid: str, entity: T) -> T: ...

    @abstractmethod
    def delete(self, uuid: str) -> bool: ...


class IAccountRepository(IBaseRepository[AccountEntity]):
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[AccountEntity]: ...


# ============================= ADAPTER LAYER =============================
class BaseRepository(IBaseRepository[T]):
    def __init__(self) -> None:
        self._storage: List[T] = []
        print("BaseRepositoryImpl initialized")

    def create(self, entity: T) -> T:
        print(f"Creating entity with uuid: {entity.uuid}")
        self._storage.append(entity)
        return entity

    def find_one(self, query: dict) -> Optional[T]:
        print(f"Finding entity with query: {query}")
        # Simulate finding logic
        if self._storage:
            return self._storage[0]
        return None

    def find_all(self) -> List[T]:
        print("Finding all entities")
        return self._storage.copy()

    def update(self, uuid: str, entity: T) -> T:
        print(f"Updating entity with uuid: {uuid}")
        # Simulate update logic
        for i, stored_entity in enumerate(self._storage):
            if stored_entity.uuid == uuid:
                self._storage[i] = entity
                break
        return entity

    def delete(self, uuid: str) -> bool:
        print(f"Deleting entity with uuid: {uuid}")
        # Simulate delete logic
        for i, entity in enumerate(self._storage):
            if entity.uuid == uuid:
                del self._storage[i]
                return True

        return False


class AccountRepositoryImpl(BaseRepository[AccountEntity], IAccountRepository):
    def __init__(self) -> None:
        super().__init__()
        print("AccountRepositoryImpl initialized")

    def find_by_email(self, email: str) -> Optional[AccountEntity]:
        print(f"Finding account by email: {email}")
        for account in self._storage:
            if account.email == email:
                return account

        # Fallback to fake data
        return AccountEntity.fake_find_one()


def main() -> None:
    account_repository: IAccountRepository = AccountRepositoryImpl()
    account = account_repository.create(
        AccountEntity(
            uuid="Ox1234567890abcdef12345678",
            email="hinsun@gmail.com",
            name="Hinsun",
            age=25,
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
        )
    )

    print(f"Created account: {account.email}")
