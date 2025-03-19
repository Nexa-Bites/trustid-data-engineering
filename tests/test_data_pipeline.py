import pytest
import os
import asyncio
from dotenv import load_dotenv

from data_ingestion import receive_verified_data, receive_verified_credentials
from data_processing import clean_data, transform_data
from storage import postgres_models, indy_ledger
from storage.database import get_db  # Ensuring DB connection loads from .env

# Load environment variables from .env
load_dotenv()

@pytest.fixture
def db_session():
    """Create a database session fixture for testing."""
    db = next(get_db())
    yield db
    db.close()

def test_clean_data():
    """Test the data cleaning functionality."""
    cleaner = clean_data.DataCleaner()
    assert cleaner.clean_name("john doe") == "John Doe"
    assert cleaner.clean_email("TEST@EXAMPLE.COM") == "test@example.com"
    assert cleaner.clean_date("2023-01-01") == "2023-01-01"
    assert cleaner.clean_phone("+12345678901") == "+12345678901"

def test_receive_user_data():
    """Test receiving user data from the backend."""
    mock_backend_url = os.getenv("MOCK_BACKEND_URL", "http://mock-backend")
    api_key = os.getenv("API_KEY", "mock_key")
    
    data = receive_verified_data.receive_data(f"{mock_backend_url}/user", api_key)
    assert "first_name" in data

def test_receive_credential_data():
    """Test receiving credential data from the backend."""
    mock_backend_url = os.getenv("MOCK_BACKEND_URL", "http://mock-backend")
    api_key = os.getenv("API_KEY", "mock_key")

    data = receive_verified_credentials.receive_credentials(f"{mock_backend_url}/credential", api_key)
    assert "credential_type" in data

@pytest.mark.asyncio
async def test_transform_data(db_session):
    """Test data transformation and storage."""
    transformer = transform_data.DataTransformer()

    # Test user transformation
    clean_user = {"first_name": "John", "last_name": "Doe", "email": "john@example.com", "dob": "1990-01-01"}
    user = await transformer.transform_user(clean_user)
    db_session.add(user)
    db_session.commit()
    assert user.user_id is not None

    # Test credential transformation
    clean_cred = {"user_id": user.user_id, "credential_type": "NationalID", "id_number": "123456789"}
    cred = await transformer.transform_credential(clean_cred, "NationalID")
    db_session.add(cred)
    db_session.commit()
    assert cred.credential_id is not None

# Run tests with: pytest tests/test_data_pipeline.py
# Load testing with Locust: locust -f tests/test_data_pipeline.py --host=http://localhost:8000
