from fastapi import FastAPI, Depends, HTTPException
from app.db import init_db
import base64
from app.config import settings
from app.schemas.key_schemas import DecryptRequest, EncryptRequest, KeyCreateRequest
from app.services.key_service import create_new_key
from app.security.auth import authenticate_service
from app.security.rbac import require_permission
from app.services.audit_service import append_audit_log
from app.repositories.audit_repo import fetch_audit_logs
from app.repositories.key_repo import get_active_key_version, get_key_metadata, revoke_key, get_key_version
from app.crypto.envelope import encrypt_with_envelope
from app.crypto.envelope import decrypt_with_envelope
from app.crypto.aes_gcm import decrypt_bytes
from app.services.key_rotation_service import rotate_key

app = FastAPI(
    title="KeyVault Lite",
    description="KeyVault Lite is a backend service that safely stores encryption keys and performs crypto operations on behalf of other services without ever exposing the keys.",
    version="0.1.5"
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "environment": settings.environment
    }

@app.post("/keys")
def create_key(
    payload: KeyCreateRequest,
    service = Depends(authenticate_service)
):
    try:
        require_permission(service["role"], "key_create")

        key_id = create_new_key(
            key_type=payload.type,
            size=payload.size,
            purpose=payload.purpose
        )

        append_audit_log(
            service_id=service["id"],
            action="key_create",
            key_id=key_id,
            key_version=1,
            result="SUCCESS"
        )

        return {"key_id": key_id}

    except Exception as e:
        append_audit_log(
            service_id=service["id"],
            action="key_create",
            key_id=None,
            key_version=None,
            result="FAILURE"
        )
        raise HTTPException(status_code=403, detail=str(e))

@app.get("/audit")
def read_audit_logs(
    limit: int = 100,
    service = Depends(authenticate_service)
):
    require_permission(service["role"], "audit_read")

    logs = fetch_audit_logs(limit)

    return [
        {
            "id": row["id"],
            "service_id": row["service_id"],
            "action": row["action"],
            "key_id": row["key_id"],
            "key_version": row["key_version"],
            "timestamp": row["timestamp"],
            "result": row["result"],
            "hash": row["hash"]
        }
        for row in logs
    ]

@app.post("/keys/{key_id}/encrypt")
def encrypt_data(
    key_id: str,
    payload: EncryptRequest,
    service = Depends(authenticate_service)
):
    require_permission(service["role"], "encrypt")

    key = get_key_metadata(key_id)
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")

    if key["status"] != "ACTIVE":
        raise HTTPException(
            status_code=403,
            detail="Key is revoked and cannot be used for encryption"
        )

    if key["purpose"] != "ENCRYPT":
        raise HTTPException(
            status_code=403,
            detail="Key not allowed for encryption"
        )

    key_row = get_active_key_version(key_id)
    if not key_row:
        # This should practically never happen, but is still correct
        raise HTTPException(
            status_code=409,
            detail="No active key version available"
        )

    kek = decrypt_bytes(settings.master_key, key_row["encrypted_key"])

    result = encrypt_with_envelope(
        plaintext=payload.plaintext.encode(),
        kek=kek
    )

    append_audit_log(
        service_id=service["id"],
        action="encrypt",
        key_id=key_id,
        key_version=key_row["version"],
        result="SUCCESS"
    )

    return {
        "ciphertext": base64.b64encode(result["ciphertext"]).decode(),
        "encrypted_dek": base64.b64encode(result["encrypted_dek"]).decode(),
        "key_version": key_row["version"]
    }

@app.post("/keys/{key_id}/decrypt")
def decrypt_data(
    key_id: str,
    payload: DecryptRequest,
    service = Depends(authenticate_service)
):
    require_permission(service["role"], "decrypt")

    key = get_key_metadata(key_id)
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")

    key_row = get_key_version(
        key_id=key_id,
        version=payload.key_version
    )
    if not key_row:
        raise HTTPException(status_code=404, detail="Key version not found")

    if key_row["status"] == "REVOKED":
        raise HTTPException(
            status_code=403,
            detail="Key version is revoked"
        )

    kek = decrypt_bytes(settings.master_key, key_row["encrypted_key"])

    plaintext = decrypt_with_envelope(
        ciphertext=base64.b64decode(payload.ciphertext),
        encrypted_dek=base64.b64decode(payload.encrypted_dek),
        kek=kek
    )

    append_audit_log(
        service_id=service["id"],
        action="decrypt",
        key_id=key_id,
        key_version=payload.key_version,
        result="SUCCESS"
    )

    return {"plaintext": plaintext.decode()}

@app.post("/keys/{key_id}/rotate")
def rotate_key_endpoint(
    key_id: str,
    service = Depends(authenticate_service)
):
    require_permission(service["role"], "key_rotate")

    key = get_key_metadata(key_id)  # simple SELECT from keys table
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")

    new_version = rotate_key(
        key_id=key_id,
        key_type=key["type"],
        size=None if key["type"] != "AES" else 256
    )

    append_audit_log(
        service_id=service["id"],
        action="key_rotate",
        key_id=key_id,
        key_version=new_version,
        result="SUCCESS"
    )

    return {
        "key_id": key_id,
        "new_version": new_version
    }

@app.post("/keys/{key_id}/revoke")
def revoke_key_endpoint(
    key_id: str,
    service = Depends(authenticate_service)
):
    require_permission(service["role"], "key_revoke")

    try:
        revoke_key(key_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    append_audit_log(
        service_id=service["id"],
        action="key_revoke",
        key_id=key_id,
        key_version=None,
        result="SUCCESS"
    )

    return {
        "key_id": key_id,
        "status": "REVOKED"
    }
