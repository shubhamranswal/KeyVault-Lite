from fastapi import FastAPI
from app.db import init_db
from app.config import settings

app = FastAPI(
    title="KeyVault Lite",
    description="Educational Key Management Service",
    version="0.1.0"
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
