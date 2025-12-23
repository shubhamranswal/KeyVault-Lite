from fastapi import FastAPI, Depends, HTTPException
from app.db import init_db
from app.config import settings
from app.schemas.key_schemas import KeyCreateRequest
from app.services.key_service import create_new_key
from app.security.auth import authenticate_service
from app.security.rbac import require_permission
from app.services.audit_service import append_audit_log
from app.repositories.audit_repo import fetch_audit_logs


app = FastAPI(
    title="KeyVault Lite",
    description="Key Management Service",
    version="0.1.1"
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