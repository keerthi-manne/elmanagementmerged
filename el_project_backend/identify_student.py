from your_app import create_app, mysql
import sys

app = create_app()

def identify():
    target = '1RV23CS007'
    with app.app_context():
        cur = mysql.connection.cursor()
        print(f"🔍 Looking for {target}...")
        
        # Exact
        cur.execute("SELECT UserID, Name, Email, Role FROM User WHERE UserID = %s", (target,))
        row = cur.fetchone()
        
        with open("whois.txt", "w", encoding="utf-8") as f:
            if row:
                f.write(f"✅ Found: {row}")
            else:
                f.write(f"❌ Not found directly.")
                
        print("Done.")

if __name__ == "__main__":
    identify()
