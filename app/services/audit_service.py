import hashlib, datetime
from app.db import get_db

def append_audit_log(service_id, action, key_id, key_version, result):
    conn = get_db()

    prev = conn.execute(
        "SELECT hash FROM audit_logs ORDER BY id DESC LIMIT 1"
    ).fetchone()
    prev_hash = prev["hash"] if prev else ""

    payload = f"{service_id}{action}{key_id}{key_version}{result}{prev_hash}"
    log_hash = hashlib.sha256(payload.encode()).hexdigest()

    conn.execute(
        """
        INSERT INTO audit_logs
        (service_id, action, key_id, key_version, timestamp, result, prev_hash, hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            service_id,
            action,
            key_id,
            key_version,
            datetime.datetime.utcnow(),
            result,
            prev_hash,
            log_hash
        )
    )
    conn.commit()
    conn.close()
