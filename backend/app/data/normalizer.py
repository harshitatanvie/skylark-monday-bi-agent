import re
from datetime import datetime
from typing import Optional, Tuple, List, Dict, Any
from app.utils.currency import parse_currency, format_inr
from app.data.schemas import (
    NormalizedDeal, 
    NormalizedWorkOrder, 
    BoardQualitySummary, 
    DataQualityReport
)

# ---------------------------------------------------------------------------
# Sector Normalization Dictionary & Rules
# ---------------------------------------------------------------------------

SECTOR_MAPPING = {
    # Energy
    "energy": "Energy",
    "energy sector": "Energy",
    "solar": "Energy",
    "renewable energy": "Energy",
    "solar / energy": "Energy",
    "power & energy": "Energy",
    "wind & solar": "Energy",
    
    # Infrastructure
    "infra": "Infrastructure",
    "infrastructure": "Infrastructure",
    "infrastructure sector": "Infrastructure",
    "roads & infra": "Infrastructure",
    "highways": "Infrastructure",
    "railways": "Infrastructure",
    
    # Construction
    "construction": "Construction",
    "construction sector": "Construction",
    "civil construction": "Construction",
    "real estate": "Construction",
    "building": "Construction",
    
    # Mining
    "mining": "Mining",
    "mining sector": "Mining",
    "coal & mining": "Mining",
    "minerals": "Mining",
    
    # Agriculture
    "agri": "Agriculture",
    "agriculture": "Agriculture",
    "agri-tech": "Agriculture",
    "farming": "Agriculture",

    # Utilities
    "utilities": "Utilities",
    "utility": "Utilities",
    "water & utilities": "Utilities",

    # Defense
    "defense": "Defense",
    "aerospace": "Defense",
    "defense & aerospace": "Defense",
}

def normalize_sector(raw_sector: Optional[str]) -> Tuple[str, bool]:
    if not raw_sector or not str(raw_sector).strip():
        return "Unspecified", False
    
    clean = str(raw_sector).strip().lower()
    clean = re.sub(r'\s+', ' ', clean)
    
    if clean in SECTOR_MAPPING:
        return SECTOR_MAPPING[clean], True
    
    # Partial matching check
    for key, canonical in SECTOR_MAPPING.items():
        if key in clean:
            return canonical, True
            
    # Capitalize cleanly if non-standard
    return clean.title(), False


# ---------------------------------------------------------------------------
# Stage & Status Normalization
# ---------------------------------------------------------------------------

DEAL_STAGE_MAPPING = {
    "closed won": "Closed Won",
    "won": "Closed Won",
    "signed": "Closed Won",
    "signed contract": "Closed Won",
    "closed-won": "Closed Won",
    
    "closed lost": "Closed Lost",
    "lost": "Closed Lost",
    "rejected": "Closed Lost",
    "closed-lost": "Closed Lost",
    "cancelled": "Closed Lost",
    
    "proposal": "Proposal Sent",
    "proposal sent": "Proposal Sent",
    "proposal submitted": "Proposal Sent",
    "quote sent": "Proposal Sent",
    
    "negotiation": "Negotiation",
    "in negotiation": "Negotiation",
    "contract review": "Negotiation",
    "legal review": "Negotiation",
    
    "qualified lead": "Qualified Lead",
    "lead": "Qualified Lead",
    "qualification": "Qualified Lead",
    "discovery": "Qualified Lead",
    "initial contact": "Qualified Lead",
}

def normalize_deal_stage(raw_stage: Optional[str]) -> Tuple[str, bool, bool, bool]:
    """Returns (normalized_stage, is_open, is_won, is_lost)"""
    if not raw_stage or not str(raw_stage).strip():
        return "Qualified Lead", True, False, False  # Default fallback open
    
    clean = str(raw_stage).strip().lower()
    stage = DEAL_STAGE_MAPPING.get(clean, "Qualified Lead")
    
    if clean in DEAL_STAGE_MAPPING:
        stage = DEAL_STAGE_MAPPING[clean]
    else:
        for k, v in DEAL_STAGE_MAPPING.items():
            if k in clean:
                stage = v
                break
    
    is_won = (stage == "Closed Won")
    is_lost = (stage == "Closed Lost")
    is_open = not (is_won or is_lost)
    
    return stage, is_open, is_won, is_lost


WORK_ORDER_STATUS_MAPPING = {
    "completed": "Completed",
    "done": "Completed",
    "finished": "Completed",
    "delivered": "Completed",
    
    "delayed": "Delayed",
    "overdue": "Delayed",
    "behind schedule": "Delayed",
    "delayed flight ops": "Delayed",
    "issues": "Delayed",
    
    "in progress": "In Progress",
    "ongoing": "In Progress",
    "flying": "In Progress",
    "in_progress": "In Progress",
    "active": "In Progress",
    "field ops": "In Progress",
    
    "on hold": "On Hold",
    "paused": "On Hold",
    "on_hold": "On Hold",
    "awaiting clearance": "On Hold",
    "weather delay": "On Hold",
    
    "not started": "Not Started",
    "pending": "Not Started",
    "scheduled": "Not Started",
    "not_started": "Not Started",
    "planning": "Not Started",
}

def normalize_work_order_status(raw_status: Optional[str]) -> Tuple[str, bool, bool, bool]:
    """Returns (normalized_status, is_active, is_completed, is_delayed)"""
    if not raw_status or not str(raw_status).strip():
        return "Not Started", True, False, False
    
    clean = str(raw_status).strip().lower()
    status = WORK_ORDER_STATUS_MAPPING.get(clean)
    
    if not status:
        for k, v in WORK_ORDER_STATUS_MAPPING.items():
            if k in clean:
                status = v
                break
    
    if not status:
        status = "In Progress"
        
    is_completed = (status == "Completed")
    is_delayed = (status == "Delayed")
    is_active = (status in ("In Progress", "Delayed", "Not Started", "On Hold"))
    
    return status, is_active, is_completed, is_delayed


# ---------------------------------------------------------------------------
# Multi-Format Date Normalizer
# ---------------------------------------------------------------------------

DATE_FORMATS = [
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%d-%b-%Y",
    "%d-%B-%Y",
    "%b %d, %Y",
    "%B %d, %Y",
    "%Y/%m/%d",
    "%d.%m.%Y",
]

def parse_date_safely(date_str: Optional[str]) -> Tuple[Optional[str], Optional[str], Optional[int]]:
    """
    Safely parses diverse date strings.
    Returns: (YYYY-MM-DD string, quarter string e.g. 'Q1-2026', year int)
    """
    if not date_str or not str(date_str).strip():
        return None, None, None
    
    clean = str(date_str).strip()
    if clean.lower() in ("null", "none", "n/a", "tbd", "pending", "-"):
        return None, None, None
    
    parsed_dt = None
    for fmt in DATE_FORMATS:
        try:
            parsed_dt = datetime.strptime(clean, fmt)
            break
        except ValueError:
            continue
            
    if not parsed_dt:
        # Regex extraction fallback for dates like "2026-03-15T00:00:00Z"
        iso_match = re.match(r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})', clean)
        if iso_match:
            try:
                y, m, d = map(int, iso_match.groups())
                parsed_dt = datetime(y, m, d)
            except ValueError:
                pass

    if not parsed_dt:
        return None, None, None

    iso_date = parsed_dt.strftime("%Y-%m-%d")
    q_num = (parsed_dt.month - 1) // 3 + 1
    quarter = f"Q{q_num}-{parsed_dt.year}"
    
    return iso_date, quarter, parsed_dt.year


# ---------------------------------------------------------------------------
# Record Normalizer Functions
# ---------------------------------------------------------------------------

def normalize_deal_record(raw: Dict[str, Any]) -> NormalizedDeal:
    issues = []
    deal_id = str(raw.get("id", "unknown"))
    name = str(raw.get("name", "Unnamed Deal")).strip()
    
    # Sector
    raw_sector = raw.get("sector")
    sector, sector_recognized = normalize_sector(raw_sector)
    if not raw_sector:
        issues.append("Missing sector")
    elif not sector_recognized:
        issues.append(f"Non-canonical sector '{raw_sector}' normalized to '{sector}'")
        
    # Amount / Deal Size
    raw_amount = raw.get("deal_size") or raw.get("amount") or raw.get("value")
    deal_size = parse_currency(raw_amount)
    if deal_size is None:
        issues.append("Missing or invalid deal size amount")
        formatted_size = "₹0"
    else:
        formatted_size = format_inr(deal_size)
        
    # Stage
    raw_stage = raw.get("stage") or raw.get("status")
    stage, is_open, is_won, is_lost = normalize_deal_stage(raw_stage)
    if not raw_stage:
        issues.append("Missing deal stage")

    # Date
    raw_date = raw.get("expected_close_date") or raw.get("close_date") or raw.get("date")
    parsed_date, quarter, year = parse_date_safely(raw_date)
    if raw_date and not parsed_date:
        issues.append(f"Unparseable expected close date: '{raw_date}'")
    elif not raw_date:
        issues.append("Missing expected close date")
        
    return NormalizedDeal(
        id=deal_id,
        name=name,
        raw_sector=str(raw_sector) if raw_sector else None,
        sector=sector,
        deal_size=deal_size,
        formatted_deal_size=formatted_size,
        raw_stage=str(raw_stage) if raw_stage else None,
        stage=stage,
        is_open=is_open,
        is_won=is_won,
        is_lost=is_lost,
        raw_expected_close_date=str(raw_date) if raw_date else None,
        expected_close_date=parsed_date,
        quarter=quarter,
        year=year,
        data_quality_issues=issues,
        is_valid=(len([i for i in issues if "Unparseable" in i or "Missing deal size" in i]) == 0)
    )


def normalize_work_order_record(raw: Dict[str, Any]) -> NormalizedWorkOrder:
    issues = []
    wo_id = str(raw.get("id", "unknown"))
    name = str(raw.get("name", "Unnamed Work Order")).strip()
    deal_name = str(raw.get("deal_name")).strip() if raw.get("deal_name") else None
    
    # Sector
    raw_sector = raw.get("sector")
    sector, sector_recognized = normalize_sector(raw_sector)
    if not raw_sector:
        issues.append("Missing sector")
    elif not sector_recognized:
        issues.append(f"Non-canonical sector '{raw_sector}' normalized to '{sector}'")

    # Status
    raw_status = raw.get("status")
    status, is_active, is_completed, is_delayed = normalize_work_order_status(raw_status)
    if not raw_status:
        issues.append("Missing work order status")
        
    # Value
    raw_val = raw.get("contract_value") or raw.get("value") or raw.get("amount")
    contract_val = parse_currency(raw_val)
    if contract_val is None:
        issues.append("Missing contract value")
        formatted_val = "₹0"
    else:
        formatted_val = format_inr(contract_val)
        
    # Dates
    raw_start = raw.get("start_date")
    start_dt, _, _ = parse_date_safely(raw_start)
    if raw_start and not start_dt:
        issues.append(f"Unparseable start date: '{raw_start}'")
        
    raw_target = raw.get("target_completion_date") or raw.get("completion_date") or raw.get("due_date")
    target_dt, _, _ = parse_date_safely(raw_target)
    if raw_target and not target_dt:
        issues.append(f"Unparseable target completion date: '{raw_target}'")
    elif not raw_target:
        issues.append("Missing target completion date")

    # Delay days calculation if dates present
    delay_days = None
    if start_dt and target_dt:
        try:
            d_start = datetime.strptime(start_dt, "%Y-%m-%d")
            d_target = datetime.strptime(target_dt, "%Y-%m-%d")
            now = datetime.now()
            if is_delayed or (now > d_target and not is_completed):
                delay_days = max(1, (now - d_target).days)
        except Exception:
            pass

    return NormalizedWorkOrder(
        id=wo_id,
        name=name,
        deal_name=deal_name,
        raw_sector=str(raw_sector) if raw_sector else None,
        sector=sector,
        raw_status=str(raw_status) if raw_status else None,
        status=status,
        is_active=is_active,
        is_completed=is_completed,
        is_delayed=is_delayed,
        contract_value=contract_val,
        formatted_contract_value=formatted_val,
        raw_start_date=str(raw_start) if raw_start else None,
        start_date=start_dt,
        raw_target_completion_date=str(raw_target) if raw_target else None,
        target_completion_date=target_dt,
        delay_days=delay_days,
        data_quality_issues=issues,
        is_valid=(len([i for i in issues if "Unparseable" in i]) == 0)
    )
