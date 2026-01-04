from your_app import create_app, mysql

app = create_app()

with app.app_context():
    cur = mysql.connection.cursor()
    
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
            print(f"{table:20s}: {count:3d} rows")
        except Exception as e:
            print(f"{table:20s}: ERROR - {str(e)[:50]}")
