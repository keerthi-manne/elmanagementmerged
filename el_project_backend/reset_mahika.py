from your_app import create_app, mysql
import bcrypt
import sys

app = create_app()
with app.app_context():
    cur = mysql.connection.cursor()
    
    email = 'mahikac.cs23@rvce.edu.in'
    print(f"Checking user: {email}")
    
    # Check if user exists
    cur.execute("SELECT UserID, Name, Role FROM User WHERE Email = %s", (email,))
    user = cur.fetchone()
    
    if not user:
        print("❌ User NOT found!")
        sys.exit(1)
        
    print(f"✅ User found: {user[1]} (Role: {user[2]})")
    
    # Generate new hash
    new_hash = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt())
    
    # Update PasswordHash column
    cur.execute("UPDATE User SET PasswordHash = %s WHERE Email = %s", (new_hash, email))
    mysql.connection.commit()
    
    print("✅ Password has been force-reset to: 123456")
