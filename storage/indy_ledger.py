from indy import IndyError, ledger, wallet, pool
import asyncio
import logging
from config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class IndyLedger:
    def __init__(self):
        self.pool_handle = None
        self.wallet_handle = None
        self.pool_name = "sovrin_stagingnet"
        self.wallet_config = {"id": settings.INDY_WALLET_ID}
        self.wallet_credentials = {"key": settings.INDY_WALLET_KEY}

    async def connect(self):
        try:
            await pool.set_protocol_version(2)
            pool_config = {"genesis_txn": "/path/to/sovrin_stagingnet.txn"}  # Replace with real path or download
            await pool.create_pool_ledger_config(self.pool_name, pool_config)
            self.pool_handle = await pool.open_pool_ledger(self.pool_name, None)
            await wallet.create_wallet(self.wallet_config, self.wallet_credentials)
            self.wallet_handle = await wallet.open_wallet(self.wallet_config, self.wallet_credentials)
            logger.info("Connected to Sovrin StagingNet")
        except IndyError as e:
            logger.error(f"Failed to connect to Indy ledger: {e}", extra={"error": str(e)})
            raise

    async def register_schema(self, schema_name: str, schema_version: str, attributes: list):
        try:
            schema_request = await ledger.build_schema_request(settings.ISSUER_DID, schema_name, schema_version, attributes)
            schema_response = await ledger.sign_and_submit_request(self.pool_handle, self.wallet_handle, settings.ISSUER_DID, schema_request)
            schema_id = schema_response["result"]["txn"]["data"]["data"]["id"]
            logger.info(f"Registered schema: {schema_name}", extra={"schema_id": schema_id})
            return schema_id
        except IndyError as e:
            logger.error(f"Schema registration failed: {e}", extra={"error": str(e)})
            raise

    async def create_credential_definition(self, schema_id: str):
        try:
            cred_def_request = await ledger.build_cred_def_request(settings.ISSUER_DID, schema_id, "TAG", "CL", {"support_revocation": True})
            cred_def_response = await ledger.sign_and_submit_request(self.pool_handle, self.wallet_handle, settings.ISSUER_DID, cred_def_request)
            cred_def_id = cred_def_response["result"]["txn"]["data"]["id"]
            logger.info(f"Created credential definition: {cred_def_id}", extra={"cred_def_id": cred_def_id})
            return cred_def_id
        except IndyError as e:
            logger.error(f"Credential definition creation failed: {e}", extra={"error": str(e)})
            raise

    async def issue_credential(self, cred_def_id: str, user_did: str, attributes: dict):
        try:
            credential_offer = await ledger.build_cred_offer_request(settings.ISSUER_DID, cred_def_id)
            credential_request = await ledger.build_cred_request(self.wallet_handle, user_did, credential_offer, cred_def_id, "master_secret")
            credential = await ledger.issue_credential(self.wallet_handle, credential_offer, credential_request, attributes)
            logger.info(f"Issued credential for user: {user_did}", extra={"cred_def_id": cred_def_id})
            return credential
        except IndyError as e:
            logger.error(f"Credential issuance failed: {e}", extra={"error": str(e)})
            raise

    async def close(self):
        if self.wallet_handle:
            await wallet.close_wallet(self.wallet_handle)
        if self.pool_handle:
            await pool.close_pool_ledger(self.pool_handle)
        logger.info("Closed Indy ledger connection")
