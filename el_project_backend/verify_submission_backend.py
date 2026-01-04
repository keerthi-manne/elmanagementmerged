import requests
import json

BASE_URL = "http://localhost:5000"

def test_submission():
    # 1. Login Merin
    print("🔑 Logging in as Merin...")
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "merinmeleet@rvce.edu.in", 
        "password": "123456"
    })
    
    if resp.status_code != 200:
        print(f"❌ Login failed: {resp.text}")
        return
        
    token = resp.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    # 2. Find Dhruti's UserID and ProjectID
    # I'll hardcode from previous steps if possible, or fetch
    # Dhruti UserID from dump: Step 504? No ID there.
    # I'll use list_students script logic or just fetch all projects
    
    print("🔍 Fetching assignments...")
    # This endpoint gets "My Assignments"
    resp = requests.get(f"{BASE_URL}/faculty/assignments", headers=headers)
    data = resp.json()
    
    # Needs to find Dhruti project
    # data has 'mentor_assignments' and 'judge_assignments'
    
    judge_assigns = data.get('judge_assignments', [])
    if not judge_assigns:
        print("❌ No judge assignments for Merin!")
        return
        
    print(f"   Found {len(judge_assigns)} judge assignments.")
    target_proj = judge_assigns[0] # Assume Dhruti is here
    pid = target_proj['ProjectID']
    print(f"   Targeting Project {pid} ({target_proj['Title']})")
    
    # We need a Student UserID on this project.
    # Helper to find student? Fetch project details?
    # /projects/<id> endpoint?
    # Or just guess from previous dump if I knew IDs.
    
    # Let's hit /projects/<id> details from faculty perspective?
    # Or assume I need to find student ID.
    # I'll try to submit for a random student ID on the project? No must be valid.
    
    # I'll use a SQL query to find Dhruti's ID first inside this script using direct DB? 
    # No, keep it pure HTTP if possible. 
    # But I can use sql helper from local.
    
    try:
        from your_app import create_app, mysql
        app = create_app()
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("SELECT UserID FROM TeamMember WHERE ProjectID = %s LIMIT 1", (pid,))
            s_row = cur.fetchone()
            if not s_row:
                print("❌ No students on project!")
                return
            student_id = s_row[0]
            print(f"   Found Student ID: {student_id}")
    except:
        print("❌ Failed to query DB for student.")
        return

    # 3. Submit Evaluation
    payload = {
        "Score": "8",
        "Feedback": "Test submission from script",
        "Phase": "Phase1",
        "StudentUserID": student_id
    }
    
    print(f"🚀 Submitting Eval for {student_id}...")
    resp = requests.post(f"{BASE_URL}/faculty/evaluate/{pid}", json=payload, headers=headers)
    
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")

if __name__ == "__main__":
    test_submission()
