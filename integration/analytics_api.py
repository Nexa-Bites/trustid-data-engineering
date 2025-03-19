import pandas as pd
from sqlalchemy.orm import Session
from storage import postgres_models
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_credential_analytics(db: Session):
    try:
        credentials = db.query(postgres_models.Credential).all()
        df = pd.DataFrame([(c.credential_id, c.created_at, c.status) for c in credentials], 
                         columns=["credential_id", "created_at", "status"])
        analytics = df.groupby("status").count().to_dict()
        logger.info("Generated credential analytics", extra={"analytics": analytics})
        return analytics
    except Exception as e:
        logger.error(f"Analytics generation failed: {e}", extra={"error": str(e)})
        raise
