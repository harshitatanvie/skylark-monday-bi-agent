import sys
from pathlib import Path

# Ensure backend root is in python path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import health, chat, leadership, metrics
from app.utils.logger import logger

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("==================================================")
    logger.info("Starting Skylark Monday.com BI Agent Backend")
    logger.info(f"Demo Mode: {settings.DEMO_MODE}")
    logger.info(f"Monday Credentials Configured: {settings.has_valid_monday_creds}")
    logger.info(f"OpenAI API Configured: {settings.has_valid_openai_key}")
    logger.info("==================================================")
    yield

app = FastAPI(
    title="Monday.com Business Intelligence Agent API",
    description="Full-stack AI-powered Business Intelligence Agent for Skylark Drones, fetching & analyzing Monday.com Deals & Work Orders boards.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(leadership.router)
app.include_router(metrics.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
