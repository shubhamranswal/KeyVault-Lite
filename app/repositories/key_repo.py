import uuid, datetime
from app.db import get_db

def create_key(key_type, purpose):
    key_id = f"key_{uuid.uuid4().hex}"
    conn = get_db()
    conn.execute(
        "INSERT INTO keys VALUES (?,?,?,?,?)",
        (key_id, key_type, purpose, "ACTIVE", datetime.datetime.utcnow())
    )
    conn.commit()
    conn.close()
    return key_id

def add_key_version(key_id, encrypted_key):
    version_id = f"ver_{uuid.uuid4().hex}"
    conn = get_db()
    conn.execute(
        """
        INSERT INTO key_versions
        VALUES (?,?,?,?,?,?)
        """,
        (
            version_id,
            key_id,
            1,
            encrypted_key,
            "ACTIVE",
            datetime.datetime.utcnow()
        )
    )
    conn.commit()
    conn.close()

def get_active_key_version(key_id: str):
    conn = get_db()
    row = conn.execute(
        """
        SELECT id, version, encrypted_key
        FROM key_versions
        WHERE key_id = ? AND status = 'ACTIVE'
        """,
        (key_id,)
    ).fetchone()
    conn.close()
    return row