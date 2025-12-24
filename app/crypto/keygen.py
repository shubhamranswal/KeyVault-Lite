import os
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives import serialization

def generate_key(key_type: str, size: int | None = None) -> bytes:
    print(f"Generating key of type {key_type} with size {size}" )
    if key_type == "AES":
        return os.urandom(size // 8)

    if key_type == "RSA":
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=size
        )
        return private_key.private_bytes(
            serialization.Encoding.DER,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption()
        )

    if key_type == "ECC":
        private_key = ec.generate_private_key(ec.SECP256R1())
        return private_key.private_bytes(
            serialization.Encoding.DER,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption()
        )

    raise ValueError("Unsupported key type")
