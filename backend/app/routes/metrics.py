from fastapi import APIRouter, Query
from typing import Optional
from app.services.analytics_service import analytics_service
from app.data.schemas import DataQualityReport

router = APIRouter(tags=["Metrics & Analytics"])

@router.get("/api/data-quality", response_model=DataQualityReport)
def get_data_quality_report(use_demo_mode: bool = Query(default=False)):
    _, _, dq = analytics_service.get_normalized_data(force_demo=use_demo_mode)
    return dq

@router.get("/api/metrics/pipeline")
def get_pipeline_metrics(use_demo_mode: bool = Query(default=False), sector: Optional[str] = None):
    return analytics_service.get_pipeline_summary(sector_filter=sector, force_demo=use_demo_mode)

@router.get("/api/metrics/revenue")
def get_revenue_metrics(use_demo_mode: bool = Query(default=False)):
    return analytics_service.get_revenue_summary(force_demo=use_demo_mode)

@router.get("/api/metrics/operations")
def get_operations_metrics(use_demo_mode: bool = Query(default=False)):
    return analytics_service.get_operational_summary(force_demo=use_demo_mode)

@router.get("/api/metrics/sectors")
def get_sector_metrics(use_demo_mode: bool = Query(default=False)):
    return analytics_service.get_sector_analytics(force_demo=use_demo_mode)
