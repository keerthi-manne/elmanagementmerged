from your_app import create_app, mysql

app = create_app()

def fix():
    with app.app_context():
        cur = mysql.connection.cursor()
        # Force AI Traffic to ML (ID 103 usually)
        cur.execute("""
            UPDATE Project p 
            JOIN Theme t ON t.ThemeName = 'Machine Learning'
            SET p.ThemeID = t.ThemeID 
            WHERE p.Title LIKE '%AI Traffic%'
        """)
        mysql.connection.commit()
        print("✅ Forced 'AI Traffic' to Machine Learning.")

if __name__ == "__main__":
    fix()
