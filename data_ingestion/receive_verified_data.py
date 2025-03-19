import logging
from pydantic import BaseModel, ValidationError
import requests
from tenacity import retry, stop_after_attempt, wait_fixed

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class UserData(BaseModel):
    first_name: str
    last_name: str
    email: str
    dob: str
    phone_number: str = None

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def receive_data(endpoint: str, api_key: str) -> dict:
    """Receives verified user data from Node.js backend."""
    try:
        response = requests.get(endpoint, headers={"Authorization": f"Bearer {api_key}"}, timeout=30, verify=True)
        response.raise_for_status()
        data = response.json()
        user_data = UserData(**data)  # Matches Node.js backend expected format
        logger.info(f"Received valid user data: {user_data}", extra={"user_data": user_data.dict()})
        return user_data.dict()
    except ValidationError as e:
        logger.error(f"Invalid data format: {e}", extra={"error": str(e)})
        raise
    except requests.RequestException as e:
        logger.error(f"API request failed: {e}", extra={"error": str(e)})
        raise
