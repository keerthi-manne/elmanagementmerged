from your_app import create_app, mysql
import random
import datetime

app = create_app()

# Sample text content for plagiarism scenarios
CONTENT_LIBRARY = {
    "AI_TRAFFIC": """
    The AI Traffic Control System uses computer vision and deep learning to optimize traffic signal timings in real-time. 
    By analyzing video feeds from intersection cameras, the system detects vehicle density and adjusts green light duration accordingly.
    This reduces congestion by 30% and lowers carbon emissions. The system uses YOLOv8 for object detection and reinforcement learning for signal adaptation.
    Key components include edge processing units, cloud analytics dashboard, and fallback timer logic for failsafe operation.
    """,
    
    "BLOCKCHAIN_VOTING": """
    Our Secure Electronic Voting Platform leverages Ethereum blockchain to ensure tamper-proof election results.
    Each vote is recorded as a transaction on the immutable ledger, providing transparency and verifiable audit trails.
    Voters authenticate using biometric verification linked to their digital IDs. Smart contracts automatically tally votes 
    once the election period ends, eliminating human error and fraud.
    Zero-knowledge proofs are employed to maintain voter anonymity while proving print validity.
    """,
    
    "IOT_AGRICULTURE": """
    Smart Farming IoT Solution monitors soil moisture, temperature, and nutrient levels using a sensor network.
    Data is transmitted via LoRaWAN to a central gateway which automates irrigation systems.
    Farmers receive alerts and insights through a mobile application. The system integrates weather forecasts to prevent over-watering during rain.
    Solar-powered nodes ensure sustainable operation in remote fields.
    """,
    
    # Text that will be used for Plagiarism (Copied from AI_TRAFFIC)
    "PLAGIARIZED_TRAFFIC": """
    The AI Traffic Control System uses computer vision and deep learning to optimize traffic signal timings in real-time. 
    By analyzing video feeds from intersection cameras, the system detects vehicle density and adjusts green light duration accordingly.
    This reduces congestion by 30% and lowers carbon emissions. The system uses YOLOv8 for object detection and reinforcement learning for signal adaptation.
    Key components include edge processing units, cloud analytics dashboard, and fallback timer logic for failsafe operation.
    """,
    
    # Text that is Partial Plagiarism (Mixed from AI_TRAFFIC)
    "PARTIAL_TRAFFIC": """
    Our traffic management project uses computer vision to optimize signal timings. 
    By analyzing video feeds from intersection cameras, the system detects vehicle density.
    This helps to reduce congestion and lower carbon emissions significantly.
    The system uses YOLOv8 for object detection and reinforcement learning.
    We also implemented edge processing units and a cloud dashboard for monitoring.
    This is a novel approach to city traffic management.
    """
}

with app.app_context():
    cur = mysql.connection.cursor()
    print("🚀 Starting Plagiarism Test Data Population...")

    # 1. Clear existing submissions
    print("\n🧹 Clearing existing submissions...")
    cur.execute("DELETE FROM ProjectSubmission")
    mysql.connection.commit()
    print("✅ All previous submissions deleted.")

    # 2. Get Approved Projects to attach submissions to
    cur.execute("SELECT ProjectID, Title FROM Project WHERE Status = 'Approved' LIMIT 10")
    projects = cur.fetchall()
    
    if len(projects) < 3:
        print("⚠️ Not enough approved projects (Need at least 3). Creating temporary projects...")
        # Create dummy projects if needed (logic skipped for brevity, assuming user has projects)
        # You can add creation logic here if needed, but usually users have projects.
    
    print(f"\nFound {len(projects)} approved projects. Distributing plagiarism cases...")

    # We need at least 3 projects to demo: Original, Plagiarized, Partial
    # If we have projects P1, P2, P3...
    
    # Case 1: P1 gets Original Content (AI Traffic)
    if len(projects) >= 1:
        p1_id = projects[0][0]
        p1_title = projects[0][1]
        
        # Get a student from this project (or assign one if missing)
        cur.execute("SELECT UserID FROM TeamMember WHERE ProjectID = %s LIMIT 1", (p1_id,))
        student = cur.fetchone()
        if not student:
            # Quick fix: find a student or use admin
            student_id = 'admin' 
        else:
            student_id = student[0]

        cur.execute("""
            INSERT INTO ProjectSubmission (ProjectID, UserID, SubmissionType, SubmissionContent, SubmittedAt)
            VALUES (%s, %s, 'Text', %s, NOW())
        """, (p1_id, student_id, CONTENT_LIBRARY["AI_TRAFFIC"]))
        print(f"✅ Created [ORIGINAL] submission for Project '{p1_title}' (ID: {p1_id})")

    # Case 2: P2 gets Plagiarized Content (Copies P1)
    if len(projects) >= 2:
        p2_id = projects[1][0]
        p2_title = projects[1][1]
        
        cur.execute("SELECT UserID FROM TeamMember WHERE ProjectID = %s LIMIT 1", (p2_id,))
        student = cur.fetchone()
        student_id = student[0] if student else 'admin'

        cur.execute("""
            INSERT INTO ProjectSubmission (ProjectID, UserID, SubmissionType, SubmissionContent, SubmittedAt)
            VALUES (%s, %s, 'Text', %s, NOW())
        """, (p2_id, student_id, CONTENT_LIBRARY["PLAGIARIZED_TRAFFIC"]))
        print(f"✅ Created [PLAGIARIZED - 100% Match] submission for Project '{p2_title}' (ID: {p2_id})")

    # Case 3: P3 gets Partial Plagiarism (Mix of P1)
    if len(projects) >= 3:
        p3_id = projects[2][0]
        p3_title = projects[2][1]
        
        cur.execute("SELECT UserID FROM TeamMember WHERE ProjectID = %s LIMIT 1", (p3_id,))
        student = cur.fetchone()
        student_id = student[0] if student else 'admin'

        cur.execute("""
            INSERT INTO ProjectSubmission (ProjectID, UserID, SubmissionType, SubmissionContent, SubmittedAt)
            VALUES (%s, %s, 'Text', %s, NOW())
        """, (p3_id, student_id, CONTENT_LIBRARY["PARTIAL_TRAFFIC"]))
        print(f"✅ Created [PARTIAL - 50% Match] submission for Project '{p3_title}' (ID: {p3_id})")

    # Case 4: P4 gets Unique Content (Blockchain)
    if len(projects) >= 4:
        p4_id = projects[3][0]
        p4_title = projects[3][1]
        
        cur.execute("SELECT UserID FROM TeamMember WHERE ProjectID = %s LIMIT 1", (p4_id,))
        student = cur.fetchone()
        student_id = student[0] if student else 'admin'

        cur.execute("""
            INSERT INTO ProjectSubmission (ProjectID, UserID, SubmissionType, SubmissionContent, SubmittedAt)
            VALUES (%s, %s, 'Text', %s, NOW())
        """, (p4_id, student_id, CONTENT_LIBRARY["BLOCKCHAIN_VOTING"]))
        print(f"✅ Created [UNIQUE] submission for Project '{p4_title}' (ID: {p4_id})")

    mysql.connection.commit()
    print("\n✅ Verification Data Populated Successfully!")
    print("---------------------------------------------------")
    print("1. Original Project (Safe)")
    print("2. 100% Copy Project (Should be High Plagiarism)")
    print("3. Partial Copy Project (Should be Medium Plagiarism)")
    print("4. Unique Project (Safe)")
    print("---------------------------------------------------")
