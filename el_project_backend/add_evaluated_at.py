from your_app import create_app, mysql

app = create_app()

def add_col():
    with app.app_context():
        cur = mysql.connection.cursor()
        try:
            cur.execute("ALTER TABLE Evaluation ADD COLUMN EvaluatedAt DATETIME DEFAULT CURRENT_TIMESTAMP")
            mysql.connection.commit()
            print("✅ Added EvaluatedAt column.")
        except Exception as e:
            print(f"⚠️ Error (maybe exists?): {e}")

if __name__ == "__main__":
    add_col()
