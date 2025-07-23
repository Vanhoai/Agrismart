import jwt
from fastapi_camelcase import CamelModel

from .cryptography import Cryptography, KeyType, KeyBackend


class JwtPayload(CamelModel):
    # JWT payload structure

    # FIXME: When add aud -> Invalid audience when decode
    iss: str  # Issuer
    aud: str  # Audience
    exp: int  # Expiration time
    iat: int  # Issued at time

    # Custom claims
    id: str
    email: str
    device_token: str


class Jwt:
    def __init__(
        self,
        cryptography: Cryptography,
    ):
        self.cryptography = cryptography

        if cryptography.backend == KeyBackend.EC:
            self.algorithm = "ES256"
        elif cryptography.backend == KeyBackend.RSA:
            self.algorithm = "RS256"

    def encode(self, payload: JwtPayload, key_type: KeyType) -> str:
        private_key = self.cryptography.load_key(key_type, is_public=False)
        token = jwt.encode(payload.model_dump(), private_key, algorithm=self.algorithm)
        return token

    def decode(self, token: str, key_type: KeyType) -> JwtPayload:
        public_key = self.cryptography.load_key(key_type, is_public=True)
        payload = jwt.decode(token, public_key, algorithms=[self.algorithm])

        print(f"Decoded payload: {payload}")
        return JwtPayload(**payload)
