
import requests
import os

BASE_URL = "http://127.0.0.1:8003"

def test_auth_flow():
    print("--- Testing Phase 9: Real Authentication ---")
    
    # 1. Register User A
    email_a = "user_a@example.com"
    pass_a = "password123"
    print(f"1. Registering {email_a}...")
    try:
        requests.post(f"{BASE_URL}/auth/register", json={"email": email_a, "password": pass_a})
    except:
        pass # Ignore if already exists

    # 2. Login User A
    print(f"2. Logging in {email_a}...")
    login_resp = requests.post(f"{BASE_URL}/auth/login", json={"email": email_a, "password": pass_a})
    if login_resp.status_code != 200:
        print(f"❌ Login Failed: {login_resp.text}")
        return
    token_a = login_resp.json()['access_token']
    headers_a = {"Authorization": f"Bearer {token_a}"}
    print("✅ Login Success")

    # 3. Upload Document as User A
    filename = "auth_test_doc.docx"
    if not os.path.exists(filename):
        from docx import Document
        doc = Document()
        doc.add_paragraph("Secret User A Content")
        doc.save(filename)
        
    print("3. Uploading document as User A...")
    with open(filename, 'rb') as f:
        files = {'file': f}
        # Note: /process endpoint expects basic auth if we didn't change it to form param.
        # Wait, Fastapi Depends(oauth2) looks for header.
        resp = requests.post(f"{BASE_URL}/process", files=files, headers=headers_a)
        
    if resp.status_code != 200:
        print(f"❌ Upload Failed: {resp.text}")
    else:
        print("✅ Upload Success")

    # 4. List Documents for User A
    print("4. Listing User A documents...")
    list_resp = requests.get(f"{BASE_URL}/documents", headers=headers_a)
    docs_a = list_resp.json()
    count_a = len(docs_a)
    print(f"   User A has {count_a} documents.")

    # 5. Register/Login User B
    email_b = "user_b@example.com"
    print(f"5. Logging in {email_b}...")
    try:
        requests.post(f"{BASE_URL}/auth/register", json={"email": email_b, "password": pass_a})
    except:
        pass
        
    login_resp_b = requests.post(f"{BASE_URL}/auth/login", json={"email": email_b, "password": pass_a})
    token_b = login_resp_b.json()['access_token']
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # 6. List Documents for User B
    print("6. Listing User B documents...")
    list_resp_b = requests.get(f"{BASE_URL}/documents", headers=headers_b)
    docs_b = list_resp_b.json()
    count_b = len(docs_b)
    print(f"   User B has {count_b} documents.")

    # Verification
    if count_a > count_b:
        print("✅ Success: User A sees their docs, User B does not.")
    else:
        # It's possible User B has old docs if we reused email, but for fresh run:
        print("⚠️  Warning: checking content isolation.")
        
    # Check if A's doc is in B's list
    # We need the filename from A's upload to be sure
    # But simply:
    user_a_files = [d['filename'] for d in docs_a]
    user_b_files = [d['filename'] for d in docs_b]
    
    # intersection
    common = set(user_a_files).intersection(set(user_b_files))
    if not common:
         print("✅ Strict Isolation Verified: No common documents.")
    else:
         print(f"❌ Isolation Failed: Found common docs: {common}")

if __name__ == "__main__":
    test_auth_flow()
