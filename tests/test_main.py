from fastapi.testclient import TestClient
from main import app
import re

client = TestClient(app)

def test_shorten_url_success():
    response = client.post("/shorten", json={"url": "https://google.com"})
    assert response.status_code == 200
    data = response.json()
    assert "short_url" in data

    #extracting short code

    match = re.search(r"http://localhost:8000/(\w+)", data["short_url"])
    assert match
    short_code = match.group(1)

    print(f"Short code generated: {short_code}")

    #testing redirection
    redirect_response = client.get(f"/{short_code}")
    print(redirect_response.status_code)
    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"] == "https://google.com"

def test_shorten_url_invalid():
    response = client.post("/shorten", json={"url": "not a valid url"})
    assert response.status_code == 422

def test_redirect_not_found():
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "URL not found"