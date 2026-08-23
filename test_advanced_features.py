import requests
import os
import time

API_URL = "http://localhost:8000"

def test_advanced_features():
    print("--- Testing Advanced Academic Features ---")
    
    # 1. Prepare test file (informal_test.docx was created in previous step)
    file_path = "informal_test.docx"
    if not os.path.exists(file_path):
        from create_test_doc import create_informal_docx
        create_informal_docx(file_path)
    
    # 2. Upload and Process
    print(f"Uploading {file_path}...")
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        data = {"style": "IEEE", "output_format": "docx"}
        response = requests.post(f"{API_URL}/process", files=files, data=data)
    
    if response.status_code != 200:
        print(f"FAILED: {response.text}")
        return

    result = response.json()
    quality = result.get("quality_report", [])
    
    print("\nIntelligent Insights Received:")
    for item in quality:
        print(f"- [{item['status'].upper()}] {item['rule']}: {item['message']}")
        if item.get("details"):
            # Print first 2 suggestions
            for d in item['details'][:2]:
                print(f"   > Suggestion: {d.get('suggestion')} for '{d.get('original')}'")

    # 3. Test Similarity (Submit same file again)
    print("\nTesting Similarity Detection (Republishing same file)...")
    with open(file_path, "rb") as f:
        files = {"file": ("duplicate.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        response = requests.post(f"{API_URL}/process", files=files, data=data)
    
    result2 = response.json()
    plag_report = next((item for item in result2.get("quality_report", []) if item["rule"] == "Plagiarism Check"), None)
    
    if plag_report:
        print(f"RESULT: {plag_report['message']}")
    else:
        print("FAILED: No plagiarism report found.")

if __name__ == "__main__":
    test_advanced_features()
