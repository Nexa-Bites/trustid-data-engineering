import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DataCleaner:
    @staticmethod
    def clean_name(name: str) -> str:
        cleaned = name.strip().title()
        if not re.match(r"^[A-Za-z \-']+$", cleaned):
            logger.error(f"Invalid name format: {name}", extra={"input": name})
            raise ValueError("Invalid name format: must contain only letters, spaces, hyphens, or apostrophes")
        return cleaned

    @staticmethod
    def clean_email(email: str) -> str:
        cleaned = email.strip().lower()
        if not re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", cleaned):
            logger.error(f"Invalid email format: {email}", extra={"input": email})
            raise ValueError("Invalid email format: must be a valid email address")
        return cleaned

    @staticmethod
    def clean_date(date_str: str) -> str:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            logger.error(f"Invalid date format: {date_str}", extra={"input": date_str})
            raise ValueError("Invalid date format: must be YYYY-MM-DD")

    @staticmethod
    def clean_phone(phone: str) -> str:
        cleaned = re.sub(r"[^\d+]", "", phone)
        if not re.match(r"^\+?[1-9]\d{7,14}$", cleaned):
            logger.error(f"Invalid phone number: {phone}", extra={"input": phone})
            raise ValueError("Invalid phone number: must be 8-15 digits, optionally starting with +")
        return cleaned
