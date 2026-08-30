from fastapi import APIRouter, HTTPException, Query
from app.data.schemas import LeadershipUpdateResponse
from app.services.ai_service import ai_agent_service
from app.utils.logger import logger

router = APIRouter(tags=["Leadership Update"])

@router.post("/api/leadership-update", response_model=LeadershipUpdateResponse)
def generate_leadership_report(use_demo_mode: bool = Query(default=False)):
    try:
        response = ai_agent_service.generate_leadership_update(force_demo=use_demo_mode)
        return response
    except Exception as e:
        logger.error(f"Error generating leadership update: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate leadership report: {str(e)}")
