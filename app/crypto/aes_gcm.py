import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt_bytes(key: bytes, plaintext: bytes) -> bytes:
    nonce = os.urandom(12)
    aes = AESGCM(key)
    ciphertext = aes.encrypt(nonce, plaintext, None)
    return nonce + ciphertext

def decrypt_bytes(key: bytes, blob: bytes) -> bytes:
    nonce = blob[:12]
    ciphertext = blob[12:]
    aes = AESGCM(key)
    return aes.decrypt(nonce, ciphertext, None)
