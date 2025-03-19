import pytest
from data_ingestion import receive_verified_data, receive_verified_credentials
from data_processing import clean_data, transform_data
from storage import postgres_models, indy_ledger
from config.database import get_db
import asyncio

@pytest.fixture
def db_session():
    db = next(get_db())
    yield db
    db.close()

def test_clean_data():
    cleaner = clean_data.DataCleaner()
    assert cleaner.clean_name("john doe") == "John Doe"
    assert cleaner.clean_email("TEST@EXAMPLE.COM") == "test@example.com"
    assert cleaner.clean_date("2023-01-01") == "2023-01-01"
    assert cleaner.clean_phone("+12345678901") == "+12345678901"

def test_receive_user_data():
    data = receive_verified_data.receive_data("http://mock-backend/user", "mock_key")
    assert "first_name" in data

def test_receive_credential_data():
    data = receive_verified_credentials.receive_credentials("http://mock-backend/credential", "mock_key")
    assert "credential_type" in data

@pytest.mark.asyncio
async def test_transform_data(db_session):
    transformer = transform_data.DataTransformer()
    clean_user = {"first_name": "John", "last_name": "Doe", "email": "john@example.com", "dob": "1990-01-01"}
    user = await transformer.transform_user(clean_user)
    db_session.add(user)
    db_session.commit()
    assert user.user_id is not None

    clean_cred = {"user_id": user.user_id, "credential_type": "NationalID", "id_number": "123456789"}
    cred = await transformer.transform_credential(clean_cred, "NationalID")
    db_session.add(cred)
    db_session.commit()
    assert cred.credential_id is not None

# Run with: pytest tests/test_data_pipeline.py
# Load testing with Locust: locust -f tests/test_data_pipeline.py --host=http://localhost:8000
