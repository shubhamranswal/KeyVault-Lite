from app.crypto.keygen import generate_key
from app.crypto.aes_gcm import encrypt_bytes
from app.config import settings
from app.repositories.key_repo import create_key, add_key_version

def create_new_key(key_type, size, purpose):
    raw_key = generate_key(key_type, size)
    encrypted = encrypt_bytes(settings.master_key, raw_key)

    key_id = create_key(key_type, purpose)
    add_key_version(key_id, encrypted)

    return key_id
