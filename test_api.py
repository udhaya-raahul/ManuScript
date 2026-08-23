import requests

url = 'http://localhost:8000/process'
files = {'file': open('test_manuscript.docx', 'rb')}

try:
    response = requests.post(url, files=files)
    if response.status_code == 200:
        print("Success: File processed successfully.")
        with open('formatted_output.docx', 'wb') as f:
            f.write(response.content)
    else:
        print(f"Error: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Exception: {e}")
