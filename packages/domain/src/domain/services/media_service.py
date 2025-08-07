from domain.usecases import UploadMediaUseCase, UploadMediaRequest

from adapters.secondary import Cloudinary, CloudinaryAsset


class MediaService(UploadMediaUseCase):
    def __init__(self):
        pass

    async def upload_media(self, media: bytes, req: UploadMediaRequest) -> CloudinaryAsset:
        json = Cloudinary.upload(file=media, folder=req.folder)
        response = CloudinaryAsset.from_json(json)
        return response
