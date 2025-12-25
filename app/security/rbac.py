ROLE_PERMISSIONS = {
    "ADMIN": {
        "key_create",
        "key_rotate",
        "key_revoke",
        "encrypt",
        "decrypt",
        "audit_read",
    },
    "SERVICE": {
        "key_create",
        "key_rotate",
        "encrypt",
        "decrypt",
    },
    "AUDITOR": {
        "audit_read",
    },
}

def require_permission(role: str, permission: str):
    if permission not in ROLE_PERMISSIONS.get(role, set()):
        raise PermissionError(f"Permission '{permission}' denied")
