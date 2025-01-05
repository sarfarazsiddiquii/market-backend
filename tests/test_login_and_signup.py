import pytest
import requests
import time

BASE_URL = "http://localhost:5000"

@pytest.fixture
def test_user():
    return {"username": "newone", "password": "00000"}

def test_signup_and_login():
    test_user = {'username': f'testuser_{int(time.time())}', 'password': '12345'}
    
    signup_response = requests.post(f"{BASE_URL}/signup", json=test_user)
    assert signup_response.status_code in [201, 400]  # Allow 400 if user exists
    if signup_response.status_code == 400:
        assert "already exists" in signup_response.json().get("error")
        
    login_response = requests.post(f"{BASE_URL}/login", json=test_user)
    assert login_response.status_code == 200
    token = login_response.json().get("access_token")   
    assert token is not None
    
    headers = {"Authorization": f"Bearer {token}"}
    profile_response = requests.get(f"{BASE_URL}/profile", headers=headers)
    assert profile_response.status_code == 200
    assert profile_response.json().get("username") == test_user["username"]