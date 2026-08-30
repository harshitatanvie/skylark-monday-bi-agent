from datetime import datetime
from fastapi import APIRouter
from app.config import settings
from app.services.monday_service import monday_service

router = APIRouter(tags=["Health & Status"])

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "Monday.com Business Intelligence Agent API",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "demo_mode": settings.DEMO_MODE,
        "has_openai": settings.has_valid_openai_key
    }

@router.get("/api/monday/status")
def monday_status():
    connected, msg = monday_service.check_connection()
    return {
        "connected": connected,
        "message": msg,
        "is_demo_mode": settings.DEMO_MODE or not settings.has_valid_monday_creds,
        "has_valid_creds": settings.has_valid_monday_creds,
        "deals_board_id": settings.MONDAY_DEALS_BOARD_ID if settings.MONDAY_DEALS_BOARD_ID else "Unconfigured (Demo Mode)",
        "work_orders_board_id": settings.MONDAY_WORK_ORDERS_BOARD_ID if settings.MONDAY_WORK_ORDERS_BOARD_ID else "Unconfigured (Demo Mode)"
    }
