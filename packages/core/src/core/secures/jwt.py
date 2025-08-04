import jwt
from fastapi_camelcase import CamelModel

from .cryptography import Cryptography, KeyType, KeyBackend


class JwtPayload(CamelModel):
    aud: str = "agrismart"  # Audience
    iss: str = "agrismart"  # Issuer
    exp: int  # Expiration time
    iat: int  # Issued at time

    jti: str
    email: str
    account_id: str

    def __init__(self, exp: int = None, iat: int = None, jti: str = None, email: str = None, account_id: str = None):
        super().__init__(
            exp=exp,
            iat=iat,
            jti=jti,
            email=email,
            account_id=account_id,
        )

    def clone(
        self,
        exp: int = None,
        iat: int = None,
        jti: str = None,
        email: str = None,
        account_id: str = None,
    ) -> "JwtPayload":
        return JwtPayload(
            exp=exp or self.exp,
            iat=iat or self.iat,
            jti=jti or self.jti,
            email=email or self.email,
            account_id=account_id or self.account_id,
        )


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
        return JwtPayload(**payload)
