import pytest
from app.data.normalizer import (
    normalize_sector, 
    normalize_deal_stage, 
    normalize_work_order_status, 
    parse_date_safely,
    normalize_deal_record,
    normalize_work_order_record
)
from app.utils.currency import parse_currency, format_inr

def test_sector_normalization():
    assert normalize_sector("Energy")[0] == "Energy"
    assert normalize_sector("energy")[0] == "Energy"
    assert normalize_sector(" ENERGY ")[0] == "Energy"
    assert normalize_sector("energy sector")[0] == "Energy"
    assert normalize_sector("infra")[0] == "Infrastructure"
    assert normalize_sector("roads & infra")[0] == "Infrastructure"
    assert normalize_sector("MINING")[0] == "Mining"
    assert normalize_sector("civil construction")[0] == "Construction"
    assert normalize_sector("Agri-Tech")[0] == "Agriculture"
    assert normalize_sector("")[0] == "Unspecified"

def test_date_parsing_multi_format():
    # YYYY-MM-DD
    dt, q, yr = parse_date_safely("2026-01-10")
    assert dt == "2026-01-10"
    assert q == "Q1-2026"
    assert yr == 2026

    # DD/MM/YYYY
    dt, q, _ = parse_date_safely("10/01/2026")
    assert dt is not None
    assert q == "Q1-2026"

    # DD-Mon-YYYY
    dt, q, _ = parse_date_safely("10-Jan-2026")
    assert dt == "2026-01-10"
    assert q == "Q1-2026"

    # Month DD, YYYY
    dt, q, _ = parse_date_safely("Jan 10, 2026")
    assert dt == "2026-01-10"

    # Invalid / Unparseable
    dt, q, _ = parse_date_safely("TBD")
    assert dt is None
    assert q is None

def test_currency_parsing():
    assert parse_currency("₹2,50,00,000") == 25000000.0
    assert parse_currency("₹1.8 Cr") == 18000000.0
    assert parse_currency("₹75,00,000") == 7500000.0
    assert parse_currency(None) is None
    assert parse_currency("N/A") is None

def test_deal_record_normalization():
    raw_deal = {
        "id": "D999",
        "name": "Test Offshore Wind Survey",
        "sector": " ENERGY ",
        "deal_size": "₹1.5 Cr",
        "stage": "Proposal Sent",
        "expected_close_date": "2026-03-30"
    }
    deal = normalize_deal_record(raw_deal)
    assert deal.id == "D999"
    assert deal.sector == "Energy"
    assert deal.deal_size == 15000000.0
    assert deal.stage == "Proposal Sent"
    assert deal.quarter == "Q1-2026"
    assert deal.is_open is True

def test_work_order_record_normalization_with_delay():
    raw_wo = {
        "id": "WO999",
        "name": "Flight Execution",
        "sector": "infra",
        "status": "Delayed Flight Ops",
        "contract_value": "₹50,00,000",
        "start_date": "2026-01-01",
        "target_completion_date": "2026-01-20"
    }
    wo = normalize_work_order_record(raw_wo)
    assert wo.sector == "Infrastructure"
    assert wo.status == "Delayed"
    assert wo.is_delayed is True
    assert wo.contract_value == 5000000.0
