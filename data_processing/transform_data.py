from uuid import uuid4
from datetime import datetime
from storage import postgres_models
from indy import IndyError, ledger
import asyncio
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DataTransformer:
    async def transform_user(self, clean_data: dict) -> postgres_models.User:
        user = postgres_models.User(
            user_id=str(uuid4()),
            first_name=clean_data["first_name"],
            last_name=clean_data["last_name"],
            email=clean_data["email"],
            dob=clean_data["dob"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        logger.info(f"Transformed user data: {user}", extra={"user_id": user.user_id})
        return user

    async def transform_credential(self, clean_data: dict, schema_name: str) -> postgres_models.Credential:
        try:
            schema_request = await ledger.build_schema_request("issuer_did", schema_name, "1.0", list(clean_data.keys()))
            schema_response = await ledger.sign_and_submit_request("pool_handle", "wallet_handle", "issuer_did", schema_request)
            schema_id = schema_response["result"]["txn"]["data"]["data"]["id"]
            logger.info(f"Registered schema: {schema_name}", extra={"schema_id": schema_id})

            cred_def_request = await ledger.build_cred_def_request("issuer_did", schema_id, "TAG", "CL", {"support_revocation": True})
            cred_def_response = await ledger.sign_and_submit_request("pool_handle", "wallet_handle", "issuer_did", cred_def_request)
            cred_def_id = cred_def_response["result"]["txn"]["data"]["id"]
            logger.info(f"Created credential definition: {cred_def_id}", extra={"cred_def_id": cred_def_id})

            credential = postgres_models.Credential(
                credential_id=str(uuid4()),
                cred_def_id=cred_def_id,
                user_id=clean_data["user_id"],
                attributes=str(clean_data),
                status="Active",
                created_at=datetime.utcnow()
            )
            logger.info(f"Transformed credential: {credential}", extra={"credential_id": credential.credential_id})
            return credential
        except IndyError as e:
            logger.error(f"Credential transformation failed: {e}", extra={"error": str(e)})
            raise
