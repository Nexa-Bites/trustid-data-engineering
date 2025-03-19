from indy import ledger, pool, wallet
from indy.error import IndyError
import asyncio
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Load required Indy-related configurations from .env
try:
    INDY_POOL_NAME = os.getenv("INDY_POOL_NAME")
    INDY_GENESIS_FILE_PATH = os.getenv("INDY_GENESIS_FILE_PATH")
    INDY_WALLET_ID = os.getenv("INDY_WALLET_ID")
    INDY_WALLET_KEY = os.getenv("INDY_WALLET_KEY")
    ISSUER_DID = os.getenv("ISSUER_DID")

    if not all([INDY_POOL_NAME, INDY_GENESIS_FILE_PATH, INDY_WALLET_ID, INDY_WALLET_KEY, ISSUER_DID]):
        raise ValueError("Missing required environment variables for Indy Ledger configuration.")
except ValueError as e:
    logger.error(str(e))
    raise

class IndyLedger:
    def __init__(self):
        self.pool_handle = None
        self.wallet_handle = None
        self.schemas = {}  # Cache for registered schemas
        self.cred_defs = {}  # Cache for credential definitions

    async def connect(self):
        """Connect to the Indy ledger."""
        try:
            await pool.set_protocol_version(2)
            pool_config = {"genesis_txn": INDY_GENESIS_FILE_PATH}
            await pool.create_pool_ledger_config(INDY_POOL_NAME, pool_config)
            self.pool_handle = await pool.open_pool_ledger(INDY_POOL_NAME, None)
            await wallet.create_wallet({"id": INDY_WALLET_ID}, {"key": INDY_WALLET_KEY})
            self.wallet_handle = await wallet.open_wallet({"id": INDY_WALLET_ID}, {"key": INDY_WALLET_KEY})
            logger.info("Connected to Indy ledger")
        except IndyError as e:
            logger.error(f"Failed to connect to Indy ledger: {e}")
            raise

    async def register_schema(self, schema_name: str, schema_version: str, attributes: list) -> str:
        """Register a schema on the Indy ledger."""
        schema_key = f"{schema_name}:{schema_version}"
        if schema_key in self.schemas:
            return self.schemas[schema_key]

        try:
            schema_request = await ledger.build_schema_request(ISSUER_DID, schema_name, schema_version, attributes)
            schema_response = await ledger.sign_and_submit_request(self.pool_handle, self.wallet_handle, ISSUER_DID, schema_request)
            schema_id = schema_response["result"]["txn"]["data"]["data"]["id"]
            self.schemas[schema_key] = schema_id
            logger.info(f"Registered schema: {schema_name} (ID: {schema_id})")
            return schema_id
        except IndyError as e:
            logger.error(f"Failed to register schema: {e}")
            raise

    async def create_credential_definition(self, schema_id: str) -> str:
        """Create a credential definition for a schema."""
        if schema_id in self.cred_defs:
            return self.cred_defs[schema_id]

        try:
            cred_def_request = await ledger.build_cred_def_request(ISSUER_DID, schema_id, "TAG", "CL", {"support_revocation": True})
            cred_def_response = await ledger.sign_and_submit_request(self.pool_handle, self.wallet_handle, ISSUER_DID, cred_def_request)
            cred_def_id = cred_def_response["result"]["txn"]["data"]["id"]
            self.cred_defs[schema_id] = cred_def_id
            logger.info(f"Created credential definition: {cred_def_id}")
            return cred_def_id
        except IndyError as e:
            logger.error(f"Failed to create credential definition: {e}")
            raise

    async def issue_credential(self, schema_name: str, schema_version: str, attributes: dict) -> dict:
        """Dynamically issue a credential."""
        try:
            # Register schema if not already registered
            schema_id = await self.register_schema(schema_name, schema_version, list(attributes.keys()))

            # Create credential definition if not already created
            cred_def_id = await self.create_credential_definition(schema_id)

            # Issue the credential
            credential_offer = await ledger.build_cred_offer(self.wallet_handle, cred_def_id)
            credential_request = await ledger.build_cred_request(self.wallet_handle, ISSUER_DID, credential_offer, cred_def_id, "master_secret")
            credential = await ledger.issue_credential(self.wallet_handle, credential_offer, credential_request, attributes)

            logger.info(f"Issued credential for schema: {schema_name}")
            return {
                "credential": credential,
                "schema_id": schema_id,
                "cred_def_id": cred_def_id,
            }
        except IndyError as e:
            logger.error(f"Failed to issue credential: {e}")
            raise

    async def close(self):
        """Close the Indy ledger connection."""
        if self.wallet_handle:
            await wallet.close_wallet(self.wallet_handle)
        if self.pool_handle:
            await pool.close_pool_ledger(self.pool_handle)
        logger.info("Closed Indy ledger connection")
