from cryptography.fernet import Fernet
from storage import openssl_keys
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DataEncryptor:
    def __init__(self):
        self.key_manager = openssl_keys.KeyManager()
        self.key = self.key_manager.get_key()
        logger.info("Initialized DataEncryptor with AWS KMS key")

    def encrypt_field(self, data: str) -> str:
        try:
            f = Fernet(self.key)
            encrypted = f.encrypt(data.encode()).decode()
            logger.info("Data encrypted successfully", extra={"data_length": len(data)})
            return encrypted
        except Exception as e:
            logger.error(f"Encryption failed: {e}", extra={"error": str(e)})
            raise

    def decrypt_field(self, encrypted_data: str) -> str:
        try:
            f = Fernet(self.key)
            decrypted = f.decrypt(encrypted_data.encode()).decode()
            logger.info("Data decrypted successfully", extra={"data_length": len(decrypted)})
            return decrypted
        except Exception as e:
            logger.error(f"Decryption failed: {e}", extra={"error": str(e)})
            raise
