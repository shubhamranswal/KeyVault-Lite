from app.db import get_db

def get_service(service_id: str):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM services WHERE id = ? AND active = 1",
        (service_id,)
    ).fetchone()
    conn.close()
    return row
