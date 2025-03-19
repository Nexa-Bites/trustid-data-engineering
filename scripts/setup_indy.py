from storage import indy_ledger
import asyncio
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def init_indy():
    try:
        logger.info("Initializing Hyperledger Indy schemas")
        indy = indy_ledger.IndyLedger()
        await indy.connect()
        await indy.register_schema("NationalID", "1.0", ["full_name", "id_number", "dob"])
        await indy.register_schema("Passport", "1.0", ["holder_name", "passport_number", "issue_date"])
        await indy.close()
        logger.info("Indy initialization complete")
    except Exception as e:
        logger.error(f"Indy setup failed: {e}", extra={"error": str(e)})
        raise

if __name__ == "__main__":
    asyncio.run(init_indy())
