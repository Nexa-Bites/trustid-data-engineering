from indy import IndyError, ledger
import asyncio
import logging
from storage import indy_ledger

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class IndyAPI:
    def __init__(self):
        self.ledger = indy_ledger.IndyLedger()

    async def verify_credential(self, credential_id: str):
        try:
            await self.ledger.connect()
            request = await ledger.build_get_cred_def_request("did", credential_id)
            response = await ledger.sign_and_submit_request(self.ledger.pool_handle, self.ledger.wallet_handle, "did", request)
            logger.info(f"Verified credential: {credential_id}", extra={"response": response})
            return response
        except IndyError as e:
            logger.error(f"Credential verification failed: {e}", extra={"error": str(e)})
            raise
        finally:
            await self.ledger.close()
