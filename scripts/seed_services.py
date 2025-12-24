from app.db import get_db

def seed_services():
    conn = get_db()

    conn.executemany(
        """
        INSERT OR IGNORE INTO services (id, name, role, active)
        VALUES (?, ?, ?, ?)
        """,
        [
            ("svc-payments", "payments-service", "SERVICE", 1),
            ("svc-auditor", "audit-service", "AUDITOR", 1),
        ]
    )

    conn.commit()
    conn.close()
    print("✅ Services seeded")

if __name__ == "__main__":
    seed_services()
