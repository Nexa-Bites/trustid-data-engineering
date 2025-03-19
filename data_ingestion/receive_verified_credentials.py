import logging
from pydantic import BaseModel, ValidationError
import requests
from tenacity import retry, stop_after_attempt, wait_fixed

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class CredentialData(BaseModel):
    credential_type: str
    holder_name: str
    attributes: dict

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def receive_credentials(endpoint: str, api_key: str) -> dict:
    """Receives verified credentials from Node.js backend."""
    try:
        response = requests.get(endpoint, headers={"Authorization": f"Bearer {api_key}"}, timeout=30, verify=True)
        response.raise_for_status()
        data = response.json()
        cred_data = CredentialData(**data)  # Matches Node.js backend expected format
        logger.info(f"Received valid credential: {cred_data}", extra={"cred_data": cred_data.dict()})
        return cred_data.dict()
    except ValidationError as e:
        logger.error(f"Invalid credential format: {e}", extra={"error": str(e)})
        raise
    except requests.RequestException as e:
        logger.error(f"API request failed: {e}", extra={"error": str(e)})
        raise
