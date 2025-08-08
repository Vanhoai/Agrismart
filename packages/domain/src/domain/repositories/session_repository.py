from domain.entities import SessionEntity
from domain.repositories import IBaseRepository


class ISessionRepository(IBaseRepository[SessionEntity]):
    pass
