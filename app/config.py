import os
import base64

class Settings:
    def __init__(self):
        key = os.getenv("KEYVAULT_MASTER_KEY")
        if not key:
            raise RuntimeError("KEYVAULT_MASTER_KEY is not set")

        try:
            decoded = base64.b64decode(key)
        except Exception:
            raise RuntimeError("KEYVAULT_MASTER_KEY must be base64 encoded")

        if len(decoded) != 32:
            raise RuntimeError("KEYVAULT_MASTER_KEY must be 32 bytes (AES-256)")

        self.master_key = decoded
        self.environment = os.getenv("ENV", "dev")

settings = Settings()
