from typing import List
from datetime import datetime
from app.data.schemas import (
    NormalizedDeal, 
    NormalizedWorkOrder, 
    BoardQualitySummary, 
    DataQualityReport
)

def build_deals_quality_summary(deals: List[NormalizedDeal]) -> BoardQualitySummary:
    total = len(deals)
    if total == 0:
        return BoardQualitySummary(board_name="Deals Board", completeness_score_pct=100.0)
    
    missing_dates = sum(1 for d in deals if not d.expected_close_date)
    missing_amounts = sum(1 for d in deals if d.deal_size is None)
    missing_status = sum(1 for d in deals if not d.raw_stage)
    unnormalized_sectors = sum(1 for d in deals if "Non-canonical" in " ".join(d.data_quality_issues))
    valid_records = sum(1 for d in deals if d.is_valid)
    
    # Weight penalties
    penalties = (missing_dates * 0.15) + (missing_amounts * 0.25) + (missing_status * 0.10)
    completeness = max(0.0, round(100.0 * (1.0 - (penalties / total)), 1))
    
    issues = []
    if missing_dates > 0:
        issues.append(f"{missing_dates} deal(s) have missing or unparseable expected close dates.")
    if missing_amounts > 0:
        issues.append(f"{missing_amounts} deal(s) have missing monetary amounts.")
    if missing_status > 0:
        issues.append(f"{missing_status} deal(s) lack stage metadata.")
    if unnormalized_sectors > 0:
        issues.append(f"{unnormalized_sectors} deal(s) used non-canonical sector names.")
        
    return BoardQualitySummary(
        board_name="Deals Board",
        total_records=total,
        valid_records=valid_records,
        missing_dates_count=missing_dates,
        missing_amounts_count=missing_amounts,
        missing_status_count=missing_status,
        unnormalized_sectors_count=unnormalized_sectors,
        completeness_score_pct=completeness,
        issues=issues
    )


def build_work_orders_quality_summary(work_orders: List[NormalizedWorkOrder]) -> BoardQualitySummary:
    total = len(work_orders)
    if total == 0:
        return BoardQualitySummary(board_name="Work Orders Board", completeness_score_pct=100.0)
    
    missing_dates = sum(1 for w in work_orders if not w.target_completion_date)
    missing_amounts = sum(1 for w in work_orders if w.contract_value is None)
    missing_status = sum(1 for w in work_orders if not w.raw_status)
    unnormalized_sectors = sum(1 for w in work_orders if "Non-canonical" in " ".join(w.data_quality_issues))
    valid_records = sum(1 for w in work_orders if w.is_valid)
    
    penalties = (missing_dates * 0.20) + (missing_amounts * 0.15) + (missing_status * 0.15)
    completeness = max(0.0, round(100.0 * (1.0 - (penalties / total)), 1))
    
    issues = []
    if missing_dates > 0:
        issues.append(f"{missing_dates} work order(s) have missing or invalid completion target dates.")
    if missing_amounts > 0:
        issues.append(f"{missing_amounts} work order(s) lack contract values.")
    if missing_status > 0:
        issues.append(f"{missing_status} work order(s) have unassigned or incomplete status.")
        
    return BoardQualitySummary(
        board_name="Work Orders Board",
        total_records=total,
        valid_records=valid_records,
        missing_dates_count=missing_dates,
        missing_amounts_count=missing_amounts,
        missing_status_count=missing_status,
        unnormalized_sectors_count=unnormalized_sectors,
        completeness_score_pct=completeness,
        issues=issues
    )


def generate_overall_data_quality_report(
    deals: List[NormalizedDeal], 
    work_orders: List[NormalizedWorkOrder]
) -> DataQualityReport:
    deals_qs = build_deals_quality_summary(deals)
    wo_qs = build_work_orders_quality_summary(work_orders)
    
    total_records = deals_qs.total_records + wo_qs.total_records
    if total_records == 0:
        overall_score = 100.0
    else:
        overall_score = round(
            (deals_qs.completeness_score_pct * deals_qs.total_records +
             wo_qs.completeness_score_pct * wo_qs.total_records) / total_records, 1
        )
        
    global_warnings = []
    if deals_qs.missing_dates_count > 0:
        global_warnings.append(f"{deals_qs.missing_dates_count} deals lack reliable close dates, which impacts quarterly sales forecasting.")
    if wo_qs.missing_dates_count > 0:
        global_warnings.append(f"{wo_qs.missing_dates_count} work orders missing target completion dates.")
    if deals_qs.missing_amounts_count > 0 or wo_qs.missing_amounts_count > 0:
        global_warnings.append(f"Monetary calculations exclude {deals_qs.missing_amounts_count + wo_qs.missing_amounts_count} records with unassigned values.")

    return DataQualityReport(
        total_records_analyzed=total_records,
        overall_health_score_pct=overall_score,
        deals_quality=deals_qs,
        work_orders_quality=wo_qs,
        global_warnings=global_warnings,
        last_fetched_timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
