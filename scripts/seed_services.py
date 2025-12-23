from app.db import get_db

def seed_auditor():
    conn = get_db()

    conn.execute(
        """
        INSERT OR IGNORE INTO services (id, name, role, active)
        VALUES (?, ?, ?, ?)
        """,
        ("svc-auditor", "audit-service", "AUDITOR", 1)
    )

    conn.commit()
    conn.close()

    print("✅ Auditor service seeded")

if __name__ == "__main__":
    seed_auditor()
