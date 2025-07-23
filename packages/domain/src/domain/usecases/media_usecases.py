from abc import ABC, abstractmethod
from typing import Literal

from fastapi_camelcase import CamelModel
from infrastructure.models import CloudinaryAsset


class UploadMediaRequest(CamelModel):
    folder: str = "common"
    media_type: Literal["image", "video", "raw", "auto"] = "auto"


class UploadMediaUseCase(ABC):
    @abstractmethod
    def upload_media(self, media: bytes, req: UploadMediaRequest) -> CloudinaryAsset: ...
