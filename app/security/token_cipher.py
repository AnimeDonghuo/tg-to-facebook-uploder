from cryptography.fernet import Fernet
from app.config import settings

class TokenCipher:
    def __init__(self, key: str):
        self.cipher = Fernet(key.encode())

    def encrypt(self, text: str) -> str:
        return self.cipher.encrypt(text.encode()).decode()

    def decrypt(self, token: str) -> str:
        return self.cipher.decrypt(token.encode()).decode()

cipher = TokenCipher(settings.TOKEN_ENCRYPTION_KEY)
