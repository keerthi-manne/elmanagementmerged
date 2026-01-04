from your_app import create_app, mysql

app = create_app()
with app.app_context():
    cur = mysql.connection.cursor()
    
    # Get one project ID
    cur.execute("SELECT ProjectID FROM Project LIMIT 1")
    project = cur.fetchone()
    if not project:
        print("No projects found!")
        exit()
    
    project_id = project[0]
    print(f"Found project ID: {project_id}")
    
    # Get one student ID
    cur.execute("SELECT UserID FROM Student LIMIT 1")
    student = cur.fetchone()
    if not student:
        print("No students found!")
        exit()
    
    student_id = student[0]
    print(f"Found student ID: {student_id}")
    
    from extensions import db
from models import User, Team, TeamMember
    print(f"\nAttempting to insert TeamMember: Project {project_id}, Student {student_id}")
    
    try:
        cur.execute("""
            INSERT INTO TeamMember (ProjectID, UserID, Role)
            VALUES (%s, %s, 'Member')
        """, (project_id, student_id))
        mysql.connection.commit()
        print("✓ SUCCESS! TeamMember inserted.")
    except Exception as e:
        print(f"✗ ERROR: {e}")
        
        # Check table structure
        print("\nChecking TeamMember table structure:")
        cur.execute("DESCRIBE TeamMember")
        for row in cur.fetchall():
            print(f"  {row}")
