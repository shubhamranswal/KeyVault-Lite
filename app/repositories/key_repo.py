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
        SELECT
            kv.id,
            kv.version,
            kv.encrypted_key,
            k.purpose
        FROM key_versions kv
        JOIN keys k ON k.id = kv.key_id
        WHERE kv.key_id = ?
          AND kv.status = 'ACTIVE'
          AND k.status = 'ACTIVE'
        """,
        (key_id,)
    ).fetchone()
    conn.close()
    return row

def rotate_key_version(key_id: str, new_encrypted_key: bytes):
    conn = get_db()

    # 1. Get current active version
    current = conn.execute(
        """
        SELECT version
        FROM key_versions
        WHERE key_id = ? AND status = 'ACTIVE'
        """,
        (key_id,)
    ).fetchone()

    if not current:
        conn.close()
        raise ValueError("No active key version found")

    new_version = current["version"] + 1

    # 2. Mark current version as ROTATED
    conn.execute(
        """
        UPDATE key_versions
        SET status = 'ROTATED'
        WHERE key_id = ? AND status = 'ACTIVE'
        """,
        (key_id,)
    )

    # 3. Insert new ACTIVE version
    conn.execute(
        """
        INSERT INTO key_versions
        VALUES (?, ?, ?, ?, 'ACTIVE', ?)
        """,
        (
            f"ver_{uuid.uuid4().hex}",
            key_id,
            new_version,
            new_encrypted_key,
            datetime.datetime.utcnow()
        )
    )

    conn.commit()
    conn.close()

    return new_version

def get_key_metadata(key_id: str):
    conn = get_db()
    row = conn.execute(
        """
        SELECT id, type, purpose, status
        FROM keys
        WHERE id = ?
        """,
        (key_id,)
    ).fetchone()
    conn.close()
    return row

def revoke_key(key_id: str):
    conn = get_db()

    result = conn.execute(
        """
        UPDATE keys
        SET status = 'REVOKED'
        WHERE id = ?
        """,
        (key_id,)
    )

    if result.rowcount == 0:
        conn.close()
        raise ValueError("Key not found or already revoked")

    conn.commit()
    conn.close()

def get_key_version(key_id: str, version: int):
    conn = get_db()
    row = conn.execute(
        """
        SELECT id, key_id, version, encrypted_key, status
        FROM key_versions
        WHERE key_id = ? AND version = ?
        """,
        (key_id, version)
    ).fetchone()
    conn.close()
    return row
