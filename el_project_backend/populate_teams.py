from your_app import create_app, mysql
import random

app = create_app()
with app.app_context():
    cur = mysql.connection.cursor()
    
    print("Populating TeamMember table...")
    
    # Clear existing team members
    cur.execute("DELETE FROM TeamMember")
    mysql.connection.commit()
    print("Cleared existing team members")
    
    # Get all projects
    cur.execute("SELECT ProjectID FROM Project")
    project_ids = [row[0] for row in cur.fetchall()]
    print(f"Found {len(project_ids)} projects")
    
    # Get all students
    cur.execute("SELECT UserID FROM Student")
    student_ids = [row[0] for row in cur.fetchall()]
    print(f"Found {len(student_ids)} students")
    
    if not project_ids or not student_ids:
        print("ERROR: No projects or students found!")
        exit()
    
    # Assign students to projects
    team_count = 0
    for project_id in project_ids:
        # Assign 1-3 students to each project
        num_members = random.randint(1, min(3, len(student_ids)))
        team_students = random.sample(student_ids, num_members)
        
        for student_id in team_students:
            try:
                cur.execute("""
                    INSERT INTO TeamMember (ProjectID, UserID)
                    VALUES (%s, %s)
                """, (project_id, student_id))
                team_count += 1
                print(f"  Added {student_id} to project {project_id}")
            except Exception as e:
                print(f"  Error adding {student_id} to project {project_id}: {e}")
    
    # Commit all changes
    mysql.connection.commit()
    print(f"\n✓ Committed {team_count} team assignments")
    
    # Verify
    cur.execute("SELECT COUNT(*) FROM TeamMember")
    final_count = cur.fetchone()[0]
    print(f"✓ Final TeamMember count: {final_count}")
