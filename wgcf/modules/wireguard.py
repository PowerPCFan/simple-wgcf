import base64
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization


class WireguardKey:
    def __init__(self, private_key_bytes: bytes | str | None = None) -> None:
        if not private_key_bytes:
            self.private_key = x25519.X25519PrivateKey.generate()
        else:
            if isinstance(private_key_bytes, str):
                private_bytes = base64.b64decode(private_key_bytes)
            else:
                private_bytes = private_key_bytes

            self.private_key = x25519.X25519PrivateKey.from_private_bytes(private_bytes)

    @staticmethod
    def generate() -> "WireguardKey":
        return WireguardKey()

    def to_base64(self) -> str:
        private_bytes = self.private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        return base64.b64encode(private_bytes).decode()

    def public_key_base64(self) -> str:
        public_key = self.private_key.public_key()
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        return base64.b64encode(public_bytes).decode()
