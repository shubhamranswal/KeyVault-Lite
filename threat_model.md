# 🔐 Threat Model — KeyVault Lite

This document outlines the security assumptions, threat model, and mitigations for KeyVault Lite.

KeyVault Lite is a **software-simulated Key Management Service**, designed for educational and demonstration purposes only.

---

## 🎯 Security Goals

1. Prevent exposure of raw cryptographic keys
2. Enforce strict access control for all key operations
3. Ensure all sensitive operations are auditable
4. Detect tampering of audit logs
5. Minimize blast radius in case of compromise

---

## 🧱 Trust Boundaries

### Trusted
- Application runtime
- Cryptographic libraries
- Master key injected via environment variable

### Untrusted / Assumed Compromised
- Database storage
- Network clients
- Client services
- Operators without explicit permissions

---

## 🗝️ Assets to Protect

| Asset | Sensitivity |
|-----|-------------|
| Master key | Critical |
| Key encryption keys (KEKs) | High |
| Data encryption keys (DEKs) | High |
| Encrypted user data | Medium |
| Audit logs | High |

---

## 👿 Threat Actors

- External attacker with DB access
- Malicious internal service
- Misconfigured service identity
- Rogue administrator
- Accidental operator error

---

## ⚠️ Threats & Mitigations

### 1. Database Compromise

**Threat:**  
Attacker gains read access to database.

**Mitigation:**
- All keys encrypted at rest
- Master key never stored in DB
- Envelope encryption limits data exposure

**Residual Risk:**  
If runtime is compromised, protection is void.

---

### 2. Key Exfiltration

**Threat:**  
Service attempts to retrieve raw key material.

**Mitigation:**
- No API exposes plaintext keys
- All cryptographic operations performed internally

**Residual Risk:**  
Malicious code in runtime can still leak memory.

---

### 3. Unauthorized Key Usage

**Threat:**  
Service uses keys beyond its intended purpose.

**Mitigation:**
- Per-service identity model
- Role-based access control
- Optional key-level access policies

---

### 4. Audit Log Tampering

**Threat:**  
Attacker modifies or deletes audit logs.

**Mitigation:**
- Append-only logs
- Hash chaining between entries
- Tampering detectable during verification

**Residual Risk:**  
Logs can still be deleted entirely by a privileged attacker.

---

### 5. Privilege Escalation

**Threat:**  
Service impersonates another service or role.

**Mitigation:**
- Explicit service identity validation
- Role-based permission checks per request

---

### 6. Key Rotation Failure

**Threat:**  
Key rotation causes loss of access to existing data.

**Mitigation:**
- Versioned keys
- Old versions retained for decryption
- Only ACTIVE version used for encryption

---

## 🚫 Explicitly Out of Scope

The following threats are **not mitigated by design**:

- Memory scraping attacks
- Side-channel attacks
- Compromised host OS
- Malicious root/admin
- Hardware-level attacks

This mirrors the threat model of most software-based KMS systems.

---

## 🧠 Security Design Trade-offs

| Decision | Trade-off |
|-------|-----------|
| Software-only KMS | No hardware guarantees |
| Env-based master key | Operational simplicity vs stronger isolation |
| Hash-chained logs | Detect tampering, not prevent it |
| SQLite support | Simplicity over horizontal scale |

---

## 🏁 Conclusion

KeyVault Lite demonstrates **realistic security engineering trade-offs** and models how modern cloud KMS systems approach:

- Key isolation
- Access mediation
- Auditability
- Damage containment

It is intentionally minimal, transparent, and explainable.

---

## ⚠️ Final Reminder

**Do not use this system to protect real secrets.**  
KeyVault Lite is an educational and portfolio project only.