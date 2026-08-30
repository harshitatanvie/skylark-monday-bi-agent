import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    MONDAY_API_TOKEN: str = os.getenv("MONDAY_API_TOKEN", "")
    MONDAY_WORK_ORDERS_BOARD_ID: str = os.getenv("MONDAY_WORK_ORDERS_BOARD_ID", "")
    MONDAY_DEALS_BOARD_ID: str = os.getenv("MONDAY_DEALS_BOARD_ID", "")
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    
    @property
    def has_valid_monday_creds(self) -> bool:
        return bool(self.MONDAY_API_TOKEN and self.MONDAY_WORK_ORDERS_BOARD_ID and self.MONDAY_DEALS_BOARD_ID)
    
    @property
    def has_valid_openai_key(self) -> bool:
        return bool(self.OPENAI_API_KEY and self.OPENAI_API_KEY.startswith("sk-"))

    @property
    def DEMO_MODE(self) -> bool:
        env_demo = os.getenv("DEMO_MODE", "").lower()
        if env_demo in ("true", "1", "yes"):
            return True
        elif env_demo in ("false", "0", "no"):
            return False
        # If valid Monday credentials are present, default to Live Mode (False).
        # Otherwise, default to Demo Mode (True).
        return not self.has_valid_monday_creds

    CORS_ORIGINS: list[str] = [
        origin.strip() for origin in os.getenv(
            "CORS_ORIGINS", 
            "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"
        ).split(",") if origin.strip()
    ]

settings = Settings()
