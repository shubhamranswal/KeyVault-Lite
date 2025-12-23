from app.db import get_db

def fetch_audit_logs(limit: int = 100):
    conn = get_db()
    rows = conn.execute(
        """
        SELECT
            id,
            service_id,
            action,
            key_id,
            key_version,
            timestamp,
            result,
            prev_hash,
            hash
        FROM audit_logs
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    ).fetchall()
    conn.close()
    return rows
