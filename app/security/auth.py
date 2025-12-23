from fastapi import Header, HTTPException, Depends
from app.repositories.service_repo import get_service

def authenticate_service(
    x_service_id: str = Header(..., alias="X-Service-Id")
):
    service = get_service(x_service_id)
    if not service:
        raise HTTPException(status_code=401, detail="Invalid service identity")
    return service
