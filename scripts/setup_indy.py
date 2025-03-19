# 📜 scripts/setup_indy.py
from storage.indy_ledger import IndyLedger
import asyncio
import logging

logger = logging.getLogger(__name__)

async def init_indy():
    """Initialize the Indy ledger with predefined schemas."""
    indy = IndyLedger()
    try:
        logger.info("Initializing Hyperledger Indy schemas")
        await indy.connect()

        # Pre-register known schemas
        schemas = [
            ("NationalID", "1.0", ["full_name", "id_number", "dob"]),
            ("Passport", "1.0", ["holder_name", "passport_number", "issue_date"]),
        ]

        for schema_name, schema_version, attributes in schemas:
            await indy.register_schema(schema_name, schema_version, attributes)

        logger.info("Indy initialization complete")
    except Exception as e:
        logger.error(f"Indy setup failed: {e}")
        raise
    finally:
        await indy.close()

if __name__ == "__main__":
    asyncio.run(init_indy())