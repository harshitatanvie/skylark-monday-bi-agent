import pytest
from app.services.analytics_service import analytics_service

def test_pipeline_summary_calculation():
    res = analytics_service.get_pipeline_summary(force_demo=True)
    assert "total_open_pipeline_val" in res
    assert res["total_open_pipeline_val"] > 0
    assert res["open_deals_count"] > 0
    assert "data_quality_report" in res
    assert res["data_quality_report"].overall_health_score_pct >= 0.0

def test_sector_analytics():
    res = analytics_service.get_sector_analytics(force_demo=True)
    assert "sectors" in res
    assert len(res["sectors"]) > 0
    assert res["strongest_pipeline_sector"] != "None"

def test_revenue_summary():
    res = analytics_service.get_revenue_summary(force_demo=True)
    assert res["won_deals_count"] > 0
    assert res["total_won_revenue_val"] > 0

def test_operational_summary_and_delays():
    res = analytics_service.get_operational_summary(force_demo=True)
    assert res["total_work_orders"] > 0
    assert "delayed_projects" in res
    assert len(res["delayed_projects"]) > 0
