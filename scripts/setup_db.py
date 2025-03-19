from alembic import command
from alembic.config import Config
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

def init_db():
    try:
        logger.info("Initializing PostgreSQL database with Alembic migrations")

        # Fetch database URL from environment variables
        database_url = os.getenv("DB_URL")

        if not database_url:
            raise ValueError("Database URL (DB_URL) is not set in the .env file")

        # Configure Alembic with the database URL
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", database_url)

        # Run migrations
        command.upgrade(alembic_cfg, "head")

        logger.info("Database initialization complete")
    except Exception as e:
        logger.error(f"Database setup failed: {e}", extra={"error": str(e)})
        raise

if __name__ == "__main__":
    init_db()
