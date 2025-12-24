from pydantic import BaseModel, field_validator
from typing import Optional

class KeyCreateRequest(BaseModel):
    type: str
    size: Optional[int] = None
    purpose: str

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str):
        v = v.upper()
        if v not in {"AES", "RSA", "ECC"}:
            raise ValueError("Unsupported key type")
        return v

    @field_validator("purpose")
    @classmethod
    def normalize_purpose(cls, v: str):
        return v.upper()

    @field_validator("size")
    @classmethod
    def validate_size(cls, v, info):
        key_type = info.data.get("type")  # ← SAFE access

        if key_type == "AES":
            if v not in (128, 256):
                raise ValueError("AES size must be 128 or 256")
            return v

        # Non-AES keys must not have size
        return None

class EncryptRequest(BaseModel):
    plaintext: str

class DecryptRequest(BaseModel):
    ciphertext: str
    encrypted_dek: str
    key_version: int
