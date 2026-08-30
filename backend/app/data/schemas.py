from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Data Models: Deals & Work Orders
# ---------------------------------------------------------------------------

class NormalizedDeal(BaseModel):
    id: str
    name: str
    raw_sector: Optional[str] = None
    sector: str  # Normalized sector (e.g. Energy, Infrastructure, Construction, etc.)
    deal_size: Optional[float] = None
    formatted_deal_size: str = "₹0"
    raw_stage: Optional[str] = None
    stage: str  # Normalized stage (Qualified Lead, Proposal Sent, Negotiation, Closed Won, Closed Lost)
    is_open: bool = True
    is_won: bool = False
    is_lost: bool = False
    raw_expected_close_date: Optional[str] = None
    expected_close_date: Optional[str] = None  # YYYY-MM-DD
    quarter: Optional[str] = None  # e.g., Q1-2026
    year: Optional[int] = None
    data_quality_issues: List[str] = Field(default_factory=list)
    is_valid: bool = True


class NormalizedWorkOrder(BaseModel):
    id: str
    name: str
    deal_name: Optional[str] = None
    raw_sector: Optional[str] = None
    sector: str  # Normalized sector
    raw_status: Optional[str] = None
    status: str  # Normalized status (Not Started, In Progress, Delayed, On Hold, Completed)
    is_active: bool = True
    is_completed: bool = False
    is_delayed: bool = False
    contract_value: Optional[float] = None
    formatted_contract_value: str = "₹0"
    raw_start_date: Optional[str] = None
    start_date: Optional[str] = None  # YYYY-MM-DD
    raw_target_completion_date: Optional[str] = None
    target_completion_date: Optional[str] = None  # YYYY-MM-DD
    delay_days: Optional[int] = None
    data_quality_issues: List[str] = Field(default_factory=list)
    is_valid: bool = True


# ---------------------------------------------------------------------------
# Data Quality Models
# ---------------------------------------------------------------------------

class BoardQualitySummary(BaseModel):
    board_name: str
    total_records: int = 0
    valid_records: int = 0
    missing_dates_count: int = 0
    missing_amounts_count: int = 0
    missing_status_count: int = 0
    unnormalized_sectors_count: int = 0
    completeness_score_pct: float = 100.0
    issues: List[str] = Field(default_factory=list)


class DataQualityReport(BaseModel):
    total_records_analyzed: int = 0
    overall_health_score_pct: float = 100.0
    deals_quality: BoardQualitySummary
    work_orders_quality: BoardQualitySummary
    global_warnings: List[str] = Field(default_factory=list)
    last_fetched_timestamp: str = ""


# ---------------------------------------------------------------------------
# Visual Analytics Models
# ---------------------------------------------------------------------------

class KPICard(BaseModel):
    title: str
    value: str
    change: Optional[str] = None
    change_type: Optional[str] = "neutral"  # positive, negative, neutral
    subtitle: Optional[str] = None


class ChartSeriesData(BaseModel):
    name: str
    value: float
    formatted_value: Optional[str] = None
    secondary_value: Optional[float] = None


class ChartSpec(BaseModel):
    title: str
    chart_type: str  # bar, pie, donut, area, line, table
    data: List[Dict[str, Any]]
    x_key: str = "name"
    y_keys: List[str] = Field(default_factory=lambda: ["value"])


# ---------------------------------------------------------------------------
# Agent Chat Request / Response Models
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    use_demo_mode: Optional[bool] = None


class ChatResponse(BaseModel):
    answer_markdown: str
    intent_detected: str
    kpi_cards: List[KPICard] = Field(default_factory=list)
    charts: List[ChartSpec] = Field(default_factory=list)
    data_quality_warning: Optional[str] = None
    data_quality_report: Optional[DataQualityReport] = None
    suggested_followups: List[str] = Field(default_factory=list)
    clarification_needed: bool = False
    clarification_options: List[str] = Field(default_factory=list)
    timestamp: str = ""
    is_demo_mode: bool = False


# ---------------------------------------------------------------------------
# Leadership Update Models
# ---------------------------------------------------------------------------

class LeadershipUpdateResponse(BaseModel):
    markdown_report: str
    executive_snapshot: Dict[str, Any]
    key_highlights: List[str]
    risks_and_attention: List[str]
    data_quality_summary: List[str]
    generated_at: str
    is_demo_mode: bool = False
