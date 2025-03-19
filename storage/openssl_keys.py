import boto3
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class KeyManager:
    def __init__(self):
        self.kms = boto3.client('kms', region_name='us-east-1')  # Configure with your AWS region
        self.key_id = self.create_key()

    def create_key(self) -> str:
        response = self.kms.create_key(
            Description='TrustID Encryption Key',
            KeyUsage='ENCRYPT_DECRYPT',
            CustomerMasterKeySpec='SYMMETRIC_DEFAULT',
            Tags=[{'TagKey': 'Project', 'TagValue': 'TrustID'}]
        )
        key_id = response['KeyMetadata']['KeyId']
        logger.info(f"Created new KMS key: {key_id}")
        return key_id

    def get_key(self) -> bytes:
        response = self.kms.generate_data_key(
            KeyId=self.key_id,
            KeySpec='AES_256'
        )
        return response['Plaintext']

    def encrypt(self, data: str) -> str:
        response = self.kms.encrypt(
            KeyId=self.key_id,
            Plaintext=data.encode()
        )
        encrypted = response['CiphertextBlob'].hex()
        logger.info("Encrypted data with KMS", extra={"data_length": len(data)})
        return encrypted

    def decrypt(self, encrypted_data: str) -> str:
        response = self.kms.decrypt(
            CiphertextBlob=bytes.fromhex(encrypted_data),
            KeyId=self.key_id
        )
        decrypted = response['Plaintext'].decode()
        logger.info("Decrypted data with KMS", extra={"data_length": len(decrypted)})
        return decrypted

    def rotate_key(self):
        old_key_id = self.key_id
        self.key_id = self.create_key()
        self.kms.schedule_key_deletion(KeyId=old_key_id, PendingWindowInDays=7)
        logger.info(f"Rotated key from {old_key_id} to {self.key_id}")
