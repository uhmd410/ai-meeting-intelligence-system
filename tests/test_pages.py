from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base, engine
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_dashboard_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Dashboard — AI Meeting Intelligence" in response.text

def test_new_meeting_page():
    response = client.get("/new-meeting")
    assert response.status_code == 200
    assert "New Meeting — AI Meeting Intelligence" in response.text

def test_history_page():
    response = client.get("/history")
    assert response.status_code == 200
    assert "Meeting History — AI Meeting Intelligence" in response.text
