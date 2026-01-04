from your_app import create_app, mysql

app = create_app()
with app.app_context():
    cur = mysql.connection.cursor()
    # Get 4 distinct projects that are Approved
    cur.execute("""
        SELECT p.ProjectID, p.Title
        FROM Project p
        WHERE p.Status = 'Approved'
        LIMIT 4
    """)
    projects = cur.fetchall()
    
    print(f"Found {len(projects)} approved projects.")
    
    for i, p in enumerate(projects):
        pid = p[0]
        title = p[1]
        
        # Get one student for this project
        cur.execute("""
            SELECT u.Name, u.Email 
            FROM TeamMember tm 
            JOIN User u ON tm.UserID = u.UserID 
            WHERE tm.ProjectID = %s 
            LIMIT 1
        """, (pid,))
        student = cur.fetchone()
        
        if student:
            print(f"Project {i+1}: {title}")
            print(f"  Student: {student[0]}")
            print(f"  Email: {student[1]}")
            print(f"  Password: 123456")
            print("-" * 30)
        else:
            print(f"Project {i+1}: {title} (No students found!)")
