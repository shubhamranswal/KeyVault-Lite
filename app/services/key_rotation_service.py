from app.crypto.keygen import generate_key
from app.crypto.aes_gcm import encrypt_bytes
from app.config import settings
from app.repositories.key_repo import rotate_key_version

def rotate_key(key_id: str, key_type: str, size: int | None):
    raw_key = generate_key(key_type, size)
    encrypted = encrypt_bytes(settings.master_key, raw_key)

    return rotate_key_version(key_id, encrypted)
