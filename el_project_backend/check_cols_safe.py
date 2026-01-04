from your_app import create_app, mysql

app = create_app()
with app.app_context():
    cur = mysql.connection.cursor()
    tables = ['MentorAssignment', 'JudgeAssignment', 'Evaluation']
    for t in tables:
        cur.execute(f"DESCRIBE {t}")
        cols = [row[0] for row in cur.fetchall()]
        print(f"{t}: {cols}")
