from alembic import command
from alembic.config import Config
import logging
from storage import postgres_models
from config import database

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def init_db():
    try:
        logger.info("Initializing PostgreSQL database with Alembic migrations")
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Database initialization complete")
    except Exception as e:
        logger.error(f"Database setup failed: {e}", extra={"error": str(e)})
        raise

if __name__ == "__main__":
    init_db()
