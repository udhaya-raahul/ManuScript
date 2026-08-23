import requests
import sys

BASE_URL = "http://localhost:8003"
EMAIL = "test_profile@example.com"
PASSWORD = "password123"
NEW_PASSWORD = "newpassword456"

def test_profile_flow():
    print("Testing Phase 10: User Profile & Security...")
    
    # 1. Register User
    print("\n1. Registering User...")
    payload = {"email": EMAIL, "password": PASSWORD, "phone": "+1234567890"}
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        if response.status_code == 200:
            print("   Registration successful.")
        elif response.status_code == 400 and "Email already registered" in response.text:
            print("   User already exists (ok for test).")
        else:
            print(f"   Registration failed: {response.text}")
            sys.exit(1)
    except Exception as e:
        print(f"   Connection failed: {e}")
        sys.exit(1)

    # 2. Login
    print("\n2. Logging in...")
    login_payload = {"email": EMAIL, "password": PASSWORD}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
    
    # If login fails, try with new password in case test ran before
    if response.status_code != 200:
        print("   Login with old password failed, trying new password...")
        login_payload["password"] = NEW_PASSWORD
        response = requests.post(f"{BASE_URL}/auth/login", json=login_payload)

    if response.status_code != 200:
        print(f"   Login failed: {response.text}")
        sys.exit(1)
        
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("   Login successful.")

    # 3. Update Profile
    print("\n3. Updating Profile...")
    profile_update = {
        "full_name": "Test User",
        "bio": "This is a test bio.",
        "organization": "Test Corp"
    }
    response = requests.put(f"{BASE_URL}/auth/profile", json=profile_update, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["full_name"] == "Test User" and data["bio"] == "This is a test bio.":
             print("   Profile update verified.")
        else:
             print(f"   Profile update mismatch: {data}")
    else:
        print(f"   Profile update failed: {response.text}")

    # 4. Fetch Profile
    print("\n4. Fetching Profile...")
    response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
    if response.status_code == 200:
        print("   Profile fetch successful.")
    else:
        print(f"   Profile fetch failed: {response.text}")

    # 5. Change Password
    print("\n5. Changing Password...")
    # Determine current password for the change request
    current_pass = NEW_PASSWORD if login_payload["password"] == NEW_PASSWORD else PASSWORD
    target_pass = PASSWORD if current_pass == NEW_PASSWORD else NEW_PASSWORD
    
    change_payload = {
        "old_password": current_pass,
        "new_password": target_pass
    }
    response = requests.post(f"{BASE_URL}/auth/change-password", json=change_payload, headers=headers)
    if response.status_code == 200:
        print("   Password change successful.")
    else:
        print(f"   Password change failed: {response.text}")

    # 6. Verify New Password Login
    print("\n6. Verifying New Password Login...")
    new_login_payload = {"email": EMAIL, "password": target_pass}
    response = requests.post(f"{BASE_URL}/auth/login", json=new_login_payload)
    if response.status_code == 200:
        print("   New password login validated.")
    else:
        print(f"   New password login failed: {response.text}")

    print("\nPhase 10 Verification Complete!")

if __name__ == "__main__":
    test_profile_flow()
