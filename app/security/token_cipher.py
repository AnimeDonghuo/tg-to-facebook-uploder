from cryptography.fernet import Fernet
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class TokenCipher:
    def __init__(self, key: str):
        try:
            self.cipher = Fernet(key.encode())
        except Exception:
            raise ValueError("Invalid TOKEN_ENCRYPTION_KEY provided.")

    def encrypt(self, plain_text: str) -> str:
        if not plain_text: return ""
        return self.cipher.encrypt(plain_text.encode()).decode()

    def decrypt(self, cipher_text: str) -> str:
        if not cipher_text: return ""
        try:
            return self.cipher.decrypt(cipher_text.encode()).decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return ""

cipher = TokenCipher(settings.TOKEN_ENCRYPTION_KEY)
