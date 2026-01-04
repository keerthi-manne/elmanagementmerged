from your_app import create_app, mysql

app = create_app()

def find_demo_context():
    with app.app_context():
        cur = mysql.connection.cursor()
        
        # 2. Find ANY Student with a Project
        cur.execute("""
            SELECT u.Name, u.Email, u.UserID, p.ProjectID, p.Title, t.ThemeName, t.ThemeID
            FROM TeamMember tm
            JOIN User u ON tm.UserID = u.UserID
            JOIN Project p ON tm.ProjectID = p.ProjectID
            JOIN Theme t ON p.ThemeID = t.ThemeID
            LIMIT 1
        """)
        
        row = cur.fetchone()
        
        if not row:
            print("❌ No students found in any projects. Please run population script.")
            return
            
        student_name, student_email, student_id, pid, ptitle, tname, tid = row
        
        print(f"✅ FOUND DEMO CONTEXT:")
        print(f"   Student: {student_name} ({student_email})")
        print(f"   Project: {ptitle} (ID: {pid})")
        print(f"   Theme:   {tname} (ID: {tid})")
        
        # 3. Suggest Faculty
        faculty_email = "merinmeleet@rvce.edu.in" 
        cur.execute("SELECT UserID, Name FROM User WHERE Email = %s", (faculty_email,))
        fac_row = cur.fetchone()
        if fac_row:
             print(f"   Faculty: {fac_row[1]} ({faculty_email}) - Use this user.")

if __name__ == "__main__":
    find_demo_context()
