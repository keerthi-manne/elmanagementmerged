from your_app import create_app, mysql

app = create_app()
with app.app_context():
    cur = mysql.connection.cursor()
    print("Checking Evaluation Schema:")
    cur.execute("DESCRIBE Evaluation")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]}")
