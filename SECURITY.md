# Security Policy

## 📢 Supported Versions

KeyVault Lite is an **educational and demonstration project**.

No versions are considered production-ready or supported for real-world use.

Security fixes may be applied on a best-effort basis, but no guarantees are made.

---

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability in KeyVault Lite:

- **Do not open a public GitHub issue**
- Report it privately via:
  - GitHub Security Advisories (preferred), or
  - Direct message to the repository maintainer

Please include:
- Description of the issue
- Steps to reproduce
- Potential impact
- Suggested mitigation (if any)

---

## 🔐 Security Scope

KeyVault Lite aims to demonstrate the following security concepts:

- Cryptographic key isolation
- Envelope encryption
- Role-based and service-based access control
- Tamper-evident audit logging

The following are **explicitly not guaranteed**:

- Protection against compromised runtime or host OS
- Hardware-backed security
- Resistance to side-channel attacks
- Protection against malicious administrators

---

## 🚫 Out of Scope

The following issues are considered **out of scope**:

- Use of KeyVault Lite in production environments
- Attacks requiring physical access
- Vulnerabilities arising from misuse or modification of the code
- Denial-of-service attacks

---

## 📦 Dependency Security

This project relies only on:
- Standard cryptographic libraries
- Actively maintained open-source dependencies

No custom cryptographic primitives are implemented.

---

## 📝 Responsible Disclosure

If a valid vulnerability is reported:
- It will be reviewed and acknowledged
- Fixes may be published publicly
- No timelines or SLAs are guaranteed

---

## ⚠️ Final Note

KeyVault Lite is intended for **learning, demonstration, and portfolio purposes only**.

Do not use this project to manage real secrets.
