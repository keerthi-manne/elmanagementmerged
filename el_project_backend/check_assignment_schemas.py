from your_app import create_app, mysql

app = create_app()
with app.app_context():
    cur = mysql.connection.cursor()
    
    tables = ['MentorAssignment', 'JudgeAssignment', 'Evaluation']
    
    for table in tables:
        print(f"\nTABLE: {table}")
        cur.execute(f"DESCRIBE {table}")
        for row in cur.fetchall():
            print(f"  {row[0]} ({row[1]})")
