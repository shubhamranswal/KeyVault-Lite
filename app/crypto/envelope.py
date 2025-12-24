import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.crypto.aes_gcm import encrypt_bytes, decrypt_bytes

def encrypt_with_envelope(plaintext: bytes, kek: bytes):
    # 1. Generate DEK
    dek = os.urandom(32)

    # 2. Encrypt data with DEK
    nonce = os.urandom(12)
    ciphertext = AESGCM(dek).encrypt(nonce, plaintext, None)

    # 3. Encrypt DEK with KEK
    encrypted_dek = encrypt_bytes(kek, dek)

    return {
        "ciphertext": nonce + ciphertext,
        "encrypted_dek": encrypted_dek
    }

def decrypt_with_envelope(ciphertext: bytes, encrypted_dek: bytes, kek: bytes):
    # 1. Decrypt DEK
    dek = decrypt_bytes(kek, encrypted_dek)

    # 2. Decrypt data
    nonce = ciphertext[:12]
    data = ciphertext[12:]

    plaintext = AESGCM(dek).decrypt(nonce, data, None)
    return plaintext
