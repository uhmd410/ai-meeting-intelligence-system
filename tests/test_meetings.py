from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_meeting_with_raw_text():
    response = client.post("/meetings", data={"title": "Test Meeting", "raw_text": "Hello, this is a test."})
    assert response.status_code == 201
    assert response.json()["status"] == "pending"

def test_create_meeting_missing_content():
    response = client.post("/meetings", data={"title": "No content"})
    assert response.status_code == 400

def test_get_nonexistent_meeting():
    response = client.get("/meetings/999999")
    assert response.status_code == 404