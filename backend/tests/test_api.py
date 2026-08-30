import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"

def test_monday_status_endpoint():
    res = client.get("/api/monday/status")
    assert res.status_code == 200
    data = res.json()
    assert "is_demo_mode" in data

def test_chat_pipeline_query():
    payload = {"message": "How is our pipeline looking this quarter?", "use_demo_mode": True}
    res = client.post("/api/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "answer_markdown" in data
    assert len(data["kpi_cards"]) > 0

def test_chat_ambiguous_query():
    payload = {"message": "how is the pipeline doing?", "use_demo_mode": True}
    res = client.post("/api/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["clarification_needed"] is True
    assert len(data["clarification_options"]) > 0

def test_leadership_update_endpoint():
    res = client.post("/api/leadership-update?use_demo_mode=true")
    assert res.status_code == 200
    data = res.json()
    assert "markdown_report" in data
    assert "EXECUTIVE LEADERSHIP UPDATE" in data["markdown_report"]
