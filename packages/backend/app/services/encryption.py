"""
Encryption Service
==================
Fernet-based encryption for sensitive fields (SSH keys, passwords).
Stores the master key in a .ai_central_key file at the backend root.
This key must NOT be committed to git.
"""

import os
from pathlib import Path

from cryptography.fernet import Fernet

_KEY_FILE = Path(__file__).resolve().parent.parent.parent / ".ai_central_key"


def _get_key() -> bytes:
    """Get encryption key from env var or file."""
    env_key = os.environ.get("AIC_ENCRYPTION_KEY")
    if env_key:
        return env_key.encode()
    if _KEY_FILE.exists():
        return _KEY_FILE.read_bytes()
    key = Fernet.generate_key()
    _KEY_FILE.write_bytes(key)
    os.chmod(_KEY_FILE, 0o600)
    return key


_cipher = Fernet(_get_key())


def encrypt(plaintext: str) -> str:
    """Encrypt a string. Returns base64-encoded ciphertext."""
    if not plaintext:
        return ""
    return _cipher.encrypt(plaintext.encode()).decode()


def decrypt(ciphertext: str) -> str:
    """Decrypt a string."""
    if not ciphertext:
        return ""
    return _cipher.decrypt(ciphertext.encode()).decode()
