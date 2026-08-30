from typing import List, Dict, Any, Optional, Tuple
from app.services.monday_service import monday_service
from app.data.normalizer import normalize_deal_record, normalize_work_order_record
from app.data.validators import generate_overall_data_quality_report
from app.data.schemas import (
    NormalizedDeal, 
    NormalizedWorkOrder, 
    DataQualityReport,
    KPICard,
    ChartSpec,
    ChartSeriesData
)
from app.utils.currency import format_inr

class AnalyticsService:
    def get_normalized_data(self, force_demo: bool = False) -> Tuple[List[NormalizedDeal], List[NormalizedWorkOrder], DataQualityReport]:
        deals_raw = monday_service.get_deals_raw(force_demo=force_demo)
        wo_raw = monday_service.get_work_orders_raw(force_demo=force_demo)
        
        normalized_deals = [normalize_deal_record(d) for d in deals_raw]
        normalized_wo = [normalize_work_order_record(w) for w in wo_raw]
        
        dq_report = generate_overall_data_quality_report(normalized_deals, normalized_wo)
        return normalized_deals, normalized_wo, dq_report

    # ---------------------------------------------------------------------------
    # 1. Pipeline Analytics
    # ---------------------------------------------------------------------------
    def get_pipeline_summary(self, sector_filter: Optional[str] = None, force_demo: bool = False) -> Dict[str, Any]:
        deals, _, dq_report = self.get_normalized_data(force_demo=force_demo)
        
        if sector_filter:
            deals = [d for d in deals if d.sector.lower() == sector_filter.lower()]
            
        total_deals_count = len(deals)
        open_deals = [d for d in deals if d.is_open]
        won_deals = [d for d in deals if d.is_won]
        lost_deals = [d for d in deals if d.is_lost]
        
        # Pipeline value calculation (Open Deals)
        open_pipeline_val = sum(d.deal_size for d in open_deals if d.deal_size is not None)
        valid_open_count = sum(1 for d in open_deals if d.deal_size is not None)
        
        # Total deal pipeline (All deals excluding lost)
        active_pipeline_val = sum(d.deal_size for d in deals if d.deal_size is not None and not d.is_lost)
        
        # Won Revenue
        won_revenue_val = sum(d.deal_size for d in won_deals if d.deal_size is not None)
        
        # Average Deal Size
        avg_deal_size = (open_pipeline_val / valid_open_count) if valid_open_count > 0 else 0.0
        
        # Win Rate
        closed_total = len(won_deals) + len(lost_deals)
        win_rate_pct = round((len(won_deals) / closed_total * 100.0), 1) if closed_total > 0 else 0.0
        
        # Quarterly Breakdown
        quarterly_dict: Dict[str, float] = {}
        for d in open_deals:
            q_key = d.quarter or "Unspecified Quarter"
            if d.deal_size is not None:
                quarterly_dict[q_key] = quarterly_dict.get(q_key, 0.0) + d.deal_size

        # Sector Breakdown
        sector_dict: Dict[str, Dict[str, Any]] = {}
        for d in open_deals:
            s = d.sector
            if s not in sector_dict:
                sector_dict[s] = {"value": 0.0, "count": 0}
            if d.deal_size is not None:
                sector_dict[s]["value"] += d.deal_size
            sector_dict[s]["count"] += 1

        # Largest Opportunities
        sorted_open_deals = sorted(open_deals, key=lambda d: d.deal_size or 0.0, reverse=True)
        top_opportunities = [
            {
                "name": d.name,
                "sector": d.sector,
                "stage": d.stage,
                "amount": format_inr(d.deal_size),
                "raw_amount": d.deal_size or 0.0,
                "expected_close": d.expected_close_date or "Missing Date"
            }
            for d in sorted_open_deals[:5]
        ]

        return {
            "total_open_pipeline_val": open_pipeline_val,
            "formatted_open_pipeline": format_inr(open_pipeline_val),
            "active_pipeline_val": active_pipeline_val,
            "formatted_active_pipeline": format_inr(active_pipeline_val),
            "won_revenue_val": won_revenue_val,
            "formatted_won_revenue": format_inr(won_revenue_val),
            "total_deals_count": total_deals_count,
            "open_deals_count": len(open_deals),
            "won_deals_count": len(won_deals),
            "lost_deals_count": len(lost_deals),
            "avg_deal_size": avg_deal_size,
            "formatted_avg_deal_size": format_inr(avg_deal_size),
            "win_rate_pct": win_rate_pct,
            "quarterly_pipeline": quarterly_dict,
            "sector_pipeline": sector_dict,
            "top_opportunities": top_opportunities,
            "data_quality_report": dq_report
        }

    # ---------------------------------------------------------------------------
    # 2. Sector Analytics
    # ---------------------------------------------------------------------------
    def get_sector_analytics(self, force_demo: bool = False) -> Dict[str, Any]:
        deals, work_orders, dq_report = self.get_normalized_data(force_demo=force_demo)
        
        sectors_dict: Dict[str, Dict[str, Any]] = {}
        
        for d in deals:
            s = d.sector
            if s not in sectors_dict:
                sectors_dict[s] = {
                    "sector": s,
                    "pipeline_val": 0.0,
                    "won_revenue_val": 0.0,
                    "open_deals_count": 0,
                    "won_deals_count": 0,
                    "work_orders_count": 0,
                    "delayed_work_orders": 0
                }
            if d.is_open and d.deal_size is not None:
                sectors_dict[s]["pipeline_val"] += d.deal_size
                sectors_dict[s]["open_deals_count"] += 1
            elif d.is_won and d.deal_size is not None:
                sectors_dict[s]["won_revenue_val"] += d.deal_size
                sectors_dict[s]["won_deals_count"] += 1
                
        for w in work_orders:
            s = w.sector
            if s not in sectors_dict:
                sectors_dict[s] = {
                    "sector": s,
                    "pipeline_val": 0.0,
                    "won_revenue_val": 0.0,
                    "open_deals_count": 0,
                    "won_deals_count": 0,
                    "work_orders_count": 0,
                    "delayed_work_orders": 0
                }
            sectors_dict[s]["work_orders_count"] += 1
            if w.is_delayed:
                sectors_dict[s]["delayed_work_orders"] += 1
                
        sector_list = list(sectors_dict.values())
        sector_list.sort(key=lambda x: x["pipeline_val"] + x["won_revenue_val"], reverse=True)
        
        # Formatting
        for s in sector_list:
            s["formatted_pipeline"] = format_inr(s["pipeline_val"])
            s["formatted_won_revenue"] = format_inr(s["won_revenue_val"])

        strongest_pipeline_sector = sector_list[0]["sector"] if sector_list else "None"

        return {
            "sectors": sector_list,
            "strongest_pipeline_sector": strongest_pipeline_sector,
            "data_quality_report": dq_report
        }

    # ---------------------------------------------------------------------------
    # 3. Revenue Analytics
    # ---------------------------------------------------------------------------
    def get_revenue_summary(self, force_demo: bool = False) -> Dict[str, Any]:
        deals, _, dq_report = self.get_normalized_data(force_demo=force_demo)
        won_deals = [d for d in deals if d.is_won]
        
        total_won_val = sum(d.deal_size for d in won_deals if d.deal_size is not None)
        avg_won_size = (total_won_val / len(won_deals)) if won_deals else 0.0
        
        # Revenue by sector
        revenue_by_sector: Dict[str, float] = {}
        for d in won_deals:
            s = d.sector
            if d.deal_size is not None:
                revenue_by_sector[s] = revenue_by_sector.get(s, 0.0) + d.deal_size
                
        sorted_rev_sectors = sorted(revenue_by_sector.items(), key=lambda x: x[1], reverse=True)
        top_revenue_sector = sorted_rev_sectors[0][0] if sorted_rev_sectors else "None"

        return {
            "total_won_revenue_val": total_won_val,
            "formatted_won_revenue": format_inr(total_won_val),
            "won_deals_count": len(won_deals),
            "avg_won_deal_size": avg_won_size,
            "formatted_avg_won_deal_size": format_inr(avg_won_size),
            "top_revenue_sector": top_revenue_sector,
            "revenue_by_sector": [
                {"sector": s, "amount": val, "formatted": format_inr(val)}
                for s, val in sorted_rev_sectors
            ],
            "data_quality_report": dq_report
        }

    # ---------------------------------------------------------------------------
    # 4. Operational & Work Orders Analytics
    # ---------------------------------------------------------------------------
    def get_operational_summary(self, force_demo: bool = False) -> Dict[str, Any]:
        _, work_orders, dq_report = self.get_normalized_data(force_demo=force_demo)
        
        total_wo = len(work_orders)
        active_wo = [w for w in work_orders if w.is_active]
        completed_wo = [w for w in work_orders if w.is_completed]
        delayed_wo = [w for w in work_orders if w.is_delayed]
        
        delay_rate_pct = round((len(delayed_wo) / total_wo * 100.0), 1) if total_wo > 0 else 0.0
        
        # Status Distribution
        status_counts: Dict[str, int] = {}
        for w in work_orders:
            st = w.status
            status_counts[st] = status_counts.get(st, 0) + 1

        # Delayed projects detail list
        delayed_projects_list = [
            {
                "id": w.id,
                "name": w.name,
                "deal_name": w.deal_name or "N/A",
                "sector": w.sector,
                "status": w.status,
                "contract_value": format_inr(w.contract_value),
                "target_completion": w.target_completion_date or "Missing Target Date",
                "delay_days": w.delay_days or 14
            }
            for w in delayed_wo
        ]

        return {
            "total_work_orders": total_wo,
            "active_work_orders_count": len(active_wo),
            "completed_work_orders_count": len(completed_wo),
            "delayed_work_orders_count": len(delayed_wo),
            "delay_rate_pct": delay_rate_pct,
            "status_distribution": status_counts,
            "delayed_projects": delayed_projects_list,
            "data_quality_report": dq_report
        }

    # ---------------------------------------------------------------------------
    # 5. Cross-Board Sales vs Execution Analytics
    # ---------------------------------------------------------------------------
    def get_cross_board_summary(self, force_demo: bool = False) -> Dict[str, Any]:
        deals, work_orders, dq_report = self.get_normalized_data(force_demo=force_demo)
        
        won_deals = [d for d in deals if d.is_won]
        total_won_revenue = sum(d.deal_size for d in won_deals if d.deal_size is not None)
        
        wo_contract_val = sum(w.contract_value for w in work_orders if w.contract_value is not None)
        
        # Sector alignment comparison
        sector_alignment: Dict[str, Dict[str, Any]] = {}
        for d in deals:
            s = d.sector
            if s not in sector_alignment:
                sector_alignment[s] = {"sector": s, "open_pipeline": 0.0, "won_revenue": 0.0, "active_ops": 0}
            if d.is_open and d.deal_size is not None:
                sector_alignment[s]["open_pipeline"] += d.deal_size
            elif d.is_won and d.deal_size is not None:
                sector_alignment[s]["won_revenue"] += d.deal_size
                
        for w in work_orders:
            s = w.sector
            if s not in sector_alignment:
                sector_alignment[s] = {"sector": s, "open_pipeline": 0.0, "won_revenue": 0.0, "active_ops": 0}
            if w.is_active:
                sector_alignment[s]["active_ops"] += 1

        alignment_list = list(sector_alignment.values())
        alignment_list.sort(key=lambda x: x["open_pipeline"] + x["won_revenue"], reverse=True)

        return {
            "total_won_deals_count": len(won_deals),
            "total_won_revenue": format_inr(total_won_revenue),
            "total_work_orders_count": len(work_orders),
            "total_work_orders_value": format_inr(wo_contract_val),
            "sector_alignment": alignment_list,
            "data_quality_report": dq_report
        }

analytics_service = AnalyticsService()
