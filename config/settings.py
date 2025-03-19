import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_USER: str = os.getenv("DB_USER", "postgres.kzlhfmtpmxhbujfengke")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "Hack#2024")
    DB_HOST: str = os.getenv("DB_HOST", "aws-0-eu-central-1.pooler.supabase.com")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_NAME: str = os.getenv("DB_NAME", "postgres")
    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

settings = Settings()
