
import requests
import sys

BASE_URL = "http://localhost:8000"

def check_endpoint(endpoint):
    url = f"{BASE_URL}{endpoint}"
    try:
        print(f"Checking {url}...", end=" ")
        resp = requests.get(url)
        if resp.status_code == 200:
            print(f"✅ OK")
            try:
                print(f"   Response: {str(resp.json())[:100]}...")
            except:
                print(f"   Response not JSON: {resp.text[:50]}...")
            return True
        else:
            print(f"❌ Failed: {resp.status_code}")
            print(f"   Error: {resp.text}")
            return False
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

def diagnose():
    print("--- Backend Diagnostics ---")
    
    # 1. Root/Docs (Implicit check if server up)
    if not check_endpoint("/docs"):
        print("CRITICAL: Server seems down or unreachable.")
        return

    # 2. Check Templates (Static data)
    check_endpoint("/templates")

    # 3. Check Activity (Database data - Suspect)
    check_endpoint("/activity")
    
    # 4. Check Documents
    check_endpoint("/documents")

if __name__ == "__main__":
    diagnose()
