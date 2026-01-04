from your_app import create_app, mysql

app = create_app()

with app.app_context():
    cur = mysql.connection.cursor()
    
    print("\n" + "="*80)
    print("DATABASE POPULATION VERIFICATION REPORT")
    print("="*80)
    
    # Table counts
    print("\nTABLE COUNTS:")
    print("-"*80)
    tables = [
        'User', 'Student', 'Faculty', 'Coordinator', 
        'Theme', 'Project', 'TeamMember', 
        'MentorAssignment', 'JudgeAssignment',
        'ProjectSubmission', 'Evaluation', 'Notification'
    ]
    
    for table in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            status = "OK" if count >= 10 else "LOW" if count > 0 else "EMPTY"
            print(f"  {status:6s} {table:20s}: {count:3d} rows")
        except Exception as e:
            print(f"  ERROR {table:20s}: {str(e)[:40]}")
    
    # Admin credentials
    print("\n" + "-"*80)
    print("ADMIN CREDENTIALS:")
    print("-"*80)
    cur.execute("SELECT UserID, Name, Email FROM User WHERE Role='Admin'")
    for row in cur.fetchall():
        print(f"  UserID: {row[0]}")
        print(f"  Name:   {row[1]}")
        print(f"  Email:  {row[2]}")
        print(f"  Password: 123456")
    
    # Faculty credentials
    print("\n" + "-"*80)
    print("FACULTY CREDENTIALS (All 10):")
    print("-"*80)
    cur.execute("SELECT U.UserID, U.Name, U.Email, F.Dept FROM User U JOIN Faculty F ON U.UserID = F.UserID WHERE U.Role='Faculty' ORDER BY U.UserID")
    faculty_data = cur.fetchall()
    for row in faculty_data:
        print(f"  ID: {row[0]:10s} | Name: {row[1]:15s} | Email: {row[2]:30s} | Dept: {row[3]} | Pass: 123456")
    
    # Student credentials
    print("\n" + "-"*80)
    print("STUDENT CREDENTIALS (All 10):")
    print("-"*80)
    cur.execute("SELECT U.UserID, U.Name, U.Email, S.Dept, S.Semester FROM User U JOIN Student S ON U.UserID = S.UserID WHERE U.Role='Student' ORDER BY U.UserID")
    student_data = cur.fetchall()
    for row in student_data:
        print(f"  ID: {row[0]:12s} | Name: {row[1]:12s} | Email: {row[2]:35s} | Dept: {row[3]:3s} | Sem: {row[4]} | Pass: 123456")
    
    # Theme summary
    print("\n" + "-"*80)
    print("THEMES:")
    print("-"*80)
    cur.execute("SELECT ThemeID, ThemeName FROM Theme ORDER BY ThemeID")
    for row in cur.fetchall():
        print(f"  {row[0]:2d}. {row[1]}")
    
    # Project summary
    print("\n" + "-"*80)
    print("PROJECTS:")
    print("-"*80)
    cur.execute("""
        SELECT P.ProjectID, P.Title, T.ThemeName, 
               (SELECT COUNT(*) FROM TeamMember WHERE ProjectID = P.ProjectID) as TeamSize
        FROM Project P
        JOIN Theme T ON P.ThemeID = T.ThemeID
        ORDER BY P.ProjectID
        LIMIT 15
    """)
    for row in cur.fetchall():
        print(f"  {row[0]:2d}. {row[1]:40s} | Theme: {row[2]:20s} | Team: {row[3]} members")
    
    print("\n" + "="*80)
    print("DATABASE VERIFICATION COMPLETE!")
    print("="*80)
    print("\nAll passwords are set to: 123456")
    print("="*80 + "\n")
