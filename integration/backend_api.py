import requests
import logging
from config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def fetch_verified_data(endpoint: str) -> dict:
    """Fetches data from Node.js backend."""
    try:
        response = requests.get(endpoint, headers={"Authorization": f"Bearer {settings.API_KEY}"}, timeout=30, verify=True)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Fetched data from backend: {data}", extra={"endpoint": endpoint})
        return data
    except requests.RequestException as e:
        logger.error(f"Backend API call failed: {e}", extra={"error": str(e)})
        raise
