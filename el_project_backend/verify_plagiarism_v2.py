import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def verify_plagiarism():
    print(f"Connecting to {BASE_URL}...")
    try:
        # Login
        resp = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "admin@rvce.edu.in", 
            "password": "123456"
        })
        print(f"Login Status: {resp.status_code}")
        if resp.status_code != 200:
            print(f"Login Error: {resp.text}")
            return
            
        token = resp.json().get('token')
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get submissions
        resp = requests.get(f"{BASE_URL}/admin/submissions/all", headers=headers)
        print("API Response:", resp.text)
        submissions = resp.json().get('submissions', [])
        
        print(f"Found {len(submissions)} submissions.")
        
        for sub in submissions[:4]:
            print(f"Checking: {sub['project_title']}")
            check = requests.post(
                f"{BASE_URL}/admin/plagiarism/check",
                json={"submission_id": sub['submission_id']},
                headers=headers
            )
            data = check.json()
            print(f"   -> Score: {data.get('plagiarism_score')}% ({data.get('status')})")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_plagiarism()
