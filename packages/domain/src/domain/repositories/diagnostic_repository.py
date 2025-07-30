from abc import ABC, abstractmethod


class DiagnosticRepository(ABC):
    @abstractmethod
    async def diagnose_rice_condition(self, image: bytes) -> str: ...
