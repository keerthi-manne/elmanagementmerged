from your_app import create_app, mysql

app = create_app()

def verify():
    with app.app_context():
        cur = mysql.connection.cursor()
        
        print("="*60)
        print("DATABASE VERIFICATION")
        print("="*60)
        
        tables_to_check = [
            'User', 'Student', 'Faculty', 'Coordinator', 'Theme', 
            'Project', 'TeamMember', 'MentorAssignment', 'JudgeAssignment',
            'ProjectSubmission', 'Evaluation', 'Notification'
        ]
        
        print("\nRECORD COUNTS:")
        for table in tables_to_check:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                count = cur.fetchone()[0]
                status = "✓" if count >= 10 else "⚠️"
                print(f"  {status} {table:20s}: {count:3d} rows")
            except Exception as e:
                print(f"  ✗ {table:20s}: ERROR - {e}")
        
        print("\nSAMPLE DATA:")
        
        # Check admin
        print("\n  Admin:")
        cur.execute("SELECT UserID, Email FROM User WHERE Role='Admin' LIMIT 1")
        admin = cur.fetchone()
        if admin:
            print(f"    ✓ {admin[0]} - {admin[1]}")
        
        # Check faculty
        print("\n  Faculty (first 3):")
        cur.execute("SELECT U.UserID, U.Email, U.Name FROM User U WHERE Role='Faculty' LIMIT 3")
        for row in cur.fetchall():
            print(f"    ✓ {row[0]} - {row[1]} - {row[2]}")
        
        # Check students
        print("\n  Students (first 3):")
        cur.execute("SELECT U.UserID, U.Email, U.Name FROM User U WHERE Role='Student' LIMIT 3")
        for row in cur.fetchall():
            print(f"    ✓ {row[0]} - {row[1]} - {row[2]}")
        
        # Check themes
        print("\n  Themes (first 3):")
        cur.execute("SELECT ThemeID, ThemeName FROM Theme LIMIT 3")
        for row in cur.fetchall():
            print(f"    ✓ {row[0]} - {row[1]}")
        
        # Check projects
        print("\n  Projects (first 3):")
        cur.execute("SELECT ProjectID, Title FROM Project LIMIT 3")
        for row in cur.fetchall():
            print(f"    ✓ {row[0]} - {row[1]}")
        
        print("\n" + "="*60)

if __name__ == '__main__':
    verify()
