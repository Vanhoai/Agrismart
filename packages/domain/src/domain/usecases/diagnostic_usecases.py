from abc import ABC, abstractmethod


class GradingDiagnosticUseCase(ABC):
    @abstractmethod
    async def diagnose(self, image: bytes) -> str: ...
