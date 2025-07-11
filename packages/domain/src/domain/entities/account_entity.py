from pydantic import EmailStr
from .base_entity import BaseEntity

class AccountEntity(BaseEntity):
    username: str
    email: str
    avatar: str
    device_token: str

    def __init__(self, username: str, email: EmailStr, avatar: str, device_token: str):
        super().__init__()
        self.username = username
        self.email = email
        self.avatar = avatar
        self.device_token = device_token

    @staticmethod
    def new(username: str, email: EmailStr, avatar: str, device_token: str):
        return AccountEntity(username, email, avatar, device_token)
