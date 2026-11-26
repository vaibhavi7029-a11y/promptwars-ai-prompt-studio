from fastapi.testclient import TestClient
from app import app, analyze_prompt

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "PromptWars" in response.text

def test_analyze_prompt():
    result = analyze_prompt("Create a study plan for beginners. Return a table with steps and success criteria.")
    assert 0 <= result["score"] <= 100
    assert "checks" in result
    assert "suggestions" in result

def test_optimize_endpoint():
    response = client.post("/api/optimize", json={
        "prompt": "Create a study plan for beginners with a weekly table and clear goals.",
        "goal": "Create a useful study plan",
        "audience": "Students",
        "tone": "Clear and professional"
    })
    assert response.status_code == 200
    assert "optimized_prompt" in response.json()
    assert "analysis" in response.json()