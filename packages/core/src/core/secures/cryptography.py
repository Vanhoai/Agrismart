import os
from enum import Enum
from loguru import logger
from typing import Optional, Tuple

from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class KeyBackend(Enum):
    RSA = "rsa"
    EC = "ec"


class KeyType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class Cryptography:
    PUBLIC_KEY_FILENAME = "public_key.pem"
    PRIVATE_KEY_FILENAME = "private_key.pem"
    RSA_KEY_SIZE = 2048

    def __init__(
        self,
        directory: str,
        backend: KeyBackend,
        is_override: bool = False,
        is_caching: bool = False,
    ) -> None:
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.directory = directory
        self.backend = backend
        self.is_override = is_override
        self.is_caching = is_caching

        self.access_private_key: Optional[str] = None
        self.access_public_key: Optional[str] = None
        self.refresh_private_key: Optional[str] = None
        self.refresh_public_key: Optional[str] = None

    def generate(self):
        if self.backend == KeyBackend.EC:
            self.generate_ec(self.directory)
        elif self.backend == KeyBackend.RSA:
            self.generate_rsa(self.directory)
        else:
            raise ValueError("Unsupported key backend.")

        # caching keypair, load 4 keys for access and refresh
        if self.is_caching:
            self.caching_keypair()

    def caching_keypair(self):
        self.access_public_key, self.access_private_key = self.load_keypair(KeyType.ACCESS)
        self.refresh_public_key, self.refresh_private_key = self.load_keypair(KeyType.REFRESH)
        logger.info("Keypair cached successfully 🐳")

    def load_keypair(self, key_type: KeyType) -> Tuple[str, str]:
        directory = os.path.join(self.directory, key_type.value)
        public_key_path = os.path.join(directory, self.PUBLIC_KEY_FILENAME)
        private_key_path = os.path.join(directory, self.PRIVATE_KEY_FILENAME)

        if not os.path.exists(public_key_path) or not os.path.exists(private_key_path):
            raise FileNotFoundError(f"Key files not found in {directory}")

        with open(public_key_path, "rb") as f:
            public_key = f.read().decode("utf-8")

        with open(private_key_path, "rb") as f:
            private_key = f.read().decode("utf-8")

        return public_key, private_key

    def generate_keypair_ec(self, directory: str) -> None:
        # Generate an EC private key
        private_key = ec.generate_private_key(
            ec.SECP256R1(),
            default_backend(),
        )

        # Derive the public key
        public_key = private_key.public_key()

        public_key_path = os.path.join(directory, Cryptography.PUBLIC_KEY_FILENAME)
        private_key_path = os.path.join(directory, Cryptography.PRIVATE_KEY_FILENAME)

        if os.path.exists(public_key_path) or os.path.exists(private_key_path):
            if self.is_override:
                logger.info(f"Keypair EC in {directory} already exists. Overriding generation 🐳")
            else:
                logger.info(f"Keypair EC in {directory} already exists. Skipping generation 🐳")
                return

        with open(private_key_path, "wb") as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )

        with open(public_key_path, "wb") as f:
            f.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )

    def generate_ec(self, directory: str) -> None:
        access_directory = os.path.join(directory, KeyType.ACCESS.value)
        refresh_directory = os.path.join(directory, KeyType.REFRESH.value)

        if not os.path.exists(access_directory):
            os.makedirs(access_directory)

        if not os.path.exists(refresh_directory):
            os.makedirs(refresh_directory)

        self.generate_keypair_ec(access_directory)
        self.generate_keypair_ec(refresh_directory)

    def generate_keypair_rsa(self, directory: str) -> None:
        # generate RSA private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=Cryptography.RSA_KEY_SIZE,
            backend=default_backend(),
        )

        # Derive the public key
        public_key = private_key.public_key()

        public_key_path = os.path.join(directory, Cryptography.PUBLIC_KEY_FILENAME)
        private_key_path = os.path.join(directory, Cryptography.PRIVATE_KEY_FILENAME)

        if os.path.exists(public_key_path) or os.path.exists(private_key_path):
            if self.is_override:
                logger.info(f"Keypair RSA in {directory} already exists. Overriding generation 🐳")
            else:
                logger.info(f"Keypair RSA in {directory} already exists. Skipping generation 🐳")
                return

        with open(private_key_path, "wb") as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )

        with open(public_key_path, "wb") as f:
            f.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )

    def generate_rsa(self, directory: str) -> None:
        access_directory = os.path.join(directory, KeyType.ACCESS.value)
        refresh_directory = os.path.join(directory, KeyType.REFRESH.value)

        if not os.path.exists(access_directory):
            os.makedirs(access_directory)

        if not os.path.exists(refresh_directory):
            os.makedirs(refresh_directory)

        self.generate_keypair_rsa(access_directory)
        self.generate_keypair_rsa(refresh_directory)

    def load_key(self, key_type: KeyType, is_public: bool) -> str:
        if self.is_caching:
            if key_type == KeyType.ACCESS:
                public_key = self.access_public_key if is_public else self.access_private_key
                if public_key is None:
                    raise ValueError("Access key not cached.")

                return public_key
            elif key_type == KeyType.REFRESH:
                public_key = self.refresh_public_key if is_public else self.refresh_private_key
                if public_key is None:
                    raise ValueError("Refresh key not cached.")

                return public_key
        else:
            directory = os.path.join(self.directory, key_type.value)
            if is_public:
                with open(os.path.join(directory, Cryptography.PUBLIC_KEY_FILENAME), "rb") as f:
                    public_key = serialization.load_pem_public_key(
                        f.read(),
                        backend=default_backend(),
                    )

                pem = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )

                return pem.decode("utf-8")

            with open(os.path.join(directory, Cryptography.PRIVATE_KEY_FILENAME), "rb") as f:
                private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=default_backend(),
                )

            pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )

            return pem.decode("utf-8")
