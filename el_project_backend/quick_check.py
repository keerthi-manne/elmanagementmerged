from your_app import create_app, mysql

app = create_app()
with app.app_context():
    cur = mysql.connection.cursor()
    
    print("\n========== QUICK VERIFICATION ==========\n")
    
    # Check admin
    cur.execute("SELECT Email FROM User WHERE Role='Admin' LIMIT 1")
    admin = cur.fetchone()
    print(f"Admin Email: {admin[0] if admin else 'NOT FOUND'}")
    
    # Check faculty count
    cur.execute("SELECT COUNT(*) FROM User WHERE Role='Faculty'")
    fac_count = cur.fetchone()[0]
    print(f"Faculty Count: {fac_count}")
    
    # Sample faculty
    cur.execute("SELECT Email FROM User WHERE Role='Faculty' LIMIT 3")
    print("Sample Faculty:")
    for row in cur.fetchall():
        print(f"  - {row[0]}")
    
    # Check student count
    cur.execute("SELECT COUNT(*) FROM User WHERE Role='Student'")
    stu_count = cur.fetchone()[0]
    print(f"\nStudent Count: {stu_count}")
    
    # Sample students
    cur.execute("SELECT Email FROM User WHERE Role='Student' LIMIT 3")
    print("Sample Students:")
    for row in cur.fetchall():
        print(f"  - {row[0]}")
    
    # Check counts for other tables
    cur.execute("SELECT COUNT(*) FROM Theme")
    print(f"\nTheme Count: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM Project")
    print(f"Project Count: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM ProjectSubmission")
    print(f"Submission Count: {cur.fetchone()[0]}")
    
    cur.execute("SELECT COUNT(*) FROM Evaluation")
    print(f"Evaluation Count: {cur.fetchone()[0]}")
    
    print("\n========================================")
    print("All passwords: 123456")
    print("========================================\n")
