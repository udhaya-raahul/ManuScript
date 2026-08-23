import requests
import time

API_URL = "http://localhost:8000"

def verify_auth():
    email = f"testuser_{int(time.time())}@example.com"
    password = "securepassword123"
    
    # Test 1: Register
    print(f"Testing Registration for {email}...")
    response = requests.post(f"{API_URL}/auth/register", json={
        "email": email,
        "password": password
    })
    
    assert response.status_code == 200, f"Registration failed: {response.text}"
    data = response.json()
    assert "access_token" in data, "No access token returned on register"
    print("Registration: OK")
    
    # Test 2: Login
    print("Testing Login...")
    response = requests.post(f"{API_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    
    assert response.status_code == 200, f"Login failed: {response.text}"
    data = response.json()
    token = data.get("access_token")
    assert token is not None, "No access token returned on login"
    print("Login: OK")
    
    # Test 3: Login with wrong password
    print("Testing Invalid Login...")
    response = requests.post(f"{API_URL}/auth/login", json={
        "email": email,
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    print("Invalid Login: OK")
    
    print("\nAll auth tests passed!")

if __name__ == "__main__":
    verify_auth()
