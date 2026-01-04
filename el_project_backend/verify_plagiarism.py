import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# Admin login to get token
def get_admin_token():
    try:
        resp = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "admin@rvce.edu.in",
            "password": "123456"
        })
        return resp.json().get('token')
    except Exception as e:
        print(f"Login failed: {e}")
        return None

def verify_plagiarism():
    token = get_admin_token()
    if not token:
        print("❌ Failed to get admin token")
        return

    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Get populated submissions to find their IDs
    print("\n🔍 Fetching latest submissions...")
    try:
        resp = requests.get(f"{BASE_URL}/admin/submissions/all", headers=headers)
        submissions = resp.json().get('submissions', [])
    except Exception as e:
        print(f"❌ Failed to fetch submissions: {e}")
        return

    if not submissions:
        print("❌ No submissions found!")
        return

    print(f"Found {len(submissions)} submissions.")

    # We expect 4 submissions from our population script.
    # Let's iterate and check their plagiarism status
    
    for sub in submissions[:4]:
        sub_id = sub['submission_id']
        project_title = sub['project_title']
        
        print(f"\n🧪 Checking plagiarism for: {project_title} (ID: {sub_id})")
        
        try:
            check_resp = requests.post(
                f"{BASE_URL}/admin/plagiarism/check", 
                json={"submission_id": sub_id},
                headers=headers
            )
            data = check_resp.json()
            
            score = data.get('plagiarism_score', 0)
            status = data.get('status', 'UNKNOWN')
            matches = data.get('matches', [])
            
            # Print results
            print(f"   Score: {score}% | Status: {status}")
            if matches:
                 print(f"   Found {len(matches)} matches:")
                 for m in matches:
                     print(f"   - Match with '{m['project_title']}' (Score: {m['similarity_score']}%)")
            else:
                print("   No plagiarism matches found.")
                
            # Basic validation based on our population logic
            # Note: Since projects ID might vary, we look at the content logic we know
            pass

        except Exception as e:
             print(f"❌ Check failed: {e}")

verify_plagiarism()
