from domain.usecases import GradingDiagnosticUseCase
from domain.repositories import DiagnosticRepository


class DiagnosticService(GradingDiagnosticUseCase):
    def __init__(self, diagnostic_repository: DiagnosticRepository) -> None:
        self.diagnostic_repository = diagnostic_repository

    async def diagnose(self, image: bytes) -> str:
        return await self.diagnostic_repository.diagnose_rice_condition(image)
