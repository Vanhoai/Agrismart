import cloudinary
from cloudinary import uploader, api
from loguru import logger

from core.configuration import Configuration


class Cloudinary:
    @staticmethod
    def setup(config: Configuration):
        cloudinary.config(
            cloud_name=config.CLOUDINARY_CLOUD_NAME,
            api_key=config.CLOUDINARY_API_KEY,
            api_secret=config.CLOUDINARY_API_SECRET,
            secure=True  # Recommended for HTTPS delivery URLs
        )

        response = api.ping()
        if response.get("status") == "ok":
            logger.info("Cloudinary is connected successfully 🌟")
        else:
            logger.error("Failed to connect to Cloudinary 😵‍💫")
            raise Exception("Cloudinary connection failed.")

    @staticmethod
    def upload(file: bytes, folder: str):
        return uploader.upload(
            file,
            folder=folder,
        )
