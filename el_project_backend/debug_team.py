from your_app import create_app, mysql

app = create_app()
with app.app_context():
    cur = mysql.connection.cursor()
    
    print("Testing TeamMember insertion...")
    print("="*50)
    
    # Check current count
    cur.execute("SELECT COUNT(*) FROM TeamMember")
    print(f"Current TeamMember count: {cur.fetchone()[0]}")
    
    # Get project and student
    cur.execute("SELECT ProjectID FROM Project LIMIT 1")
    project_id = cur.fetchone()[0]
    
    cur.execute("SELECT UserID FROM Student LIMIT 1")
    student_id = cur.fetchone()[0]
    
    print(f"Project: {project_id}, Student: {student_id}")
    
    # Show table structure
    print("\nTeamMember table structure:")
    cur.execute("SHOW CREATE TABLE TeamMember")
    print(cur.fetchone()[1])
    
    # Try insert
    print(f"\nInserting...")
    try:
        cur.execute("""
            INSERT INTO TeamMember (ProjectID, UserID, Role)
            VALUES (%s, %s, 'Member')
        """, (project_id, student_id))
        print(f"Insert executed, rows affected: {cur.rowcount}")
        
        mysql.connection.commit()
        print("Committed!")
        
        # Check count again
        cur.execute("SELECT COUNT(*) FROM TeamMember")
        print(f"TeamMember count after insert: {cur.fetchone()[0]}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
