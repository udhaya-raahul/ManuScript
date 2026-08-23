
import requests
import os

BASE_URL = "http://localhost:8003"
TEST_USER_EMAIL = "colleague@example.com"

def test_share_flow():
    print("--- Testing Phase 8: Collaboration Hub ---")
    
    # 1. Upload a document (to get an ID)
    filename = "test_share_doc.docx"
    if not os.path.exists(filename):
        from docx import Document
        doc = Document()
        doc.add_paragraph("Confidential Project Data")
        doc.save(filename)
        
    print("1. Uploading document...")
    with open(filename, 'rb') as f:
        files = {'file': f}
        resp = requests.post(f"{BASE_URL}/process", files=files)
        
    if resp.status_code != 200:
        print(f"❌ Upload Failed: {resp.text}")
        return

    # To get ID, we need to fetch activity or documents list
    # Assuming the latest one is ours
    print("2. Fetching document ID...")
    docs_resp = requests.get(f"{BASE_URL}/documents") # /documents returns all
    docs = docs_resp.json()
    if not docs:
        print("❌ No documents found")
        return
        
    # Get ID of the last one
    target_doc = docs[0] # Ordered desc
    doc_id = target_doc['id']
    print(f"   Target Document ID: {doc_id} ({target_doc['filename']})")

    # 3. Share it
    print(f"3. Sharing with {TEST_USER_EMAIL}...")
    share_payload = {
        "document_id": doc_id,
        "email": TEST_USER_EMAIL,
        "permission": "edit"
    }
    share_resp = requests.post(f"{BASE_URL}/share", json=share_payload)
    if share_resp.status_code == 200:
        print(f"✅ Share Success: {share_resp.json()}")
    else:
        print(f"❌ Share Failed: {share_resp.text}")
        return

    # 4. Verify Shared List
    print("4. Verifying 'Shared With Me' list...")
    list_resp = requests.get(f"{BASE_URL}/shared_documents?user_email={TEST_USER_EMAIL}")
    shared_list = list_resp.json()
    
    found = False
    for item in shared_list:
        if item['id'] == doc_id:
            found = True
            print(f"✅ Found shared document: {item['filename']} (Permission: {item['permission']})")
            break
            
    if not found:
        print("❌ Document NOT found in shared list")
    
if __name__ == "__main__":
    test_share_flow()
