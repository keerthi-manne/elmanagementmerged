from your_app import create_app, mysql

app = create_app()

def debug_khushi():
    with app.app_context():
        cur = mysql.connection.cursor()
        print("🔍 Checking Dhruti and Khushi Team Status...")
        
        # 1. Get IDs for Dhruti and Khushi
        # Assuming emails based on previous dumb
        emails = {
            'Dhruti': 'dhrutic.cs23@rvce.edu.in',
            'Khushi': 'khushii.is23@rvce.edu.in'
        }
        
        users = {}
        for name, email in emails.items():
            cur.execute("SELECT UserID, Name FROM User WHERE Email = %s", (email,))
            row = cur.fetchone()
            if row:
                users[name] = row[0]
                print(f"   Found {name}: {row[0]}")
            else:
                print(f"❌ Could not find {name} ({email})")
                return

        # 2. Check their Projects
        pids = {}
        for name, uid in users.items():
            cur.execute("""
                SELECT p.ProjectID, p.Title, tm.TeamID 
                FROM TeamMember tm 
                JOIN Project p ON tm.ProjectID = p.ProjectID
                WHERE tm.UserID = %s
            """, (uid,))
            row = cur.fetchone()
            if row:
                pids[name] = row
                print(f"   {name} is on Project {row[0]}: '{row[1]}' (TeamID: {row[2]})")
            else:
                pids[name] = None
                print(f"   {name} has NO project.")

        # 3. Analyze Discrepancy
        d_proj = pids['Dhruti']
        k_proj = pids['Khushi']
        
        if d_proj and k_proj:
            if d_proj[0] != k_proj[0]:
                print(f"⚠️ MISMATCH! Same Title? {d_proj[1] == k_proj[1]}")
                print(f"   Dhruti is on {d_proj[0]}, Khushi is on {k_proj[0]}.")
                
                # Check Judge for Dhruti's project
                cur.execute("SELECT FacultyUserID FROM JudgeAssignment WHERE ProjectID = %s", (d_proj[0],))
                judge = cur.fetchone()
                print(f"   Judge for Dhruti (Proj {d_proj[0]}): {judge}")
                
                # FIX: Move Khushi to Dhruti's project
                print("🔧 Moving Khushi to Dhruti's project...")
                try:
                    # Delete old
                    cur.execute("DELETE FROM TeamMember WHERE UserID = %s", (users['Khushi'],))
                    # Insert new
                    cur.execute("INSERT INTO TeamMember (UserID, ProjectID) VALUES (%s, %s)", (users['Khushi'], d_proj[0]))
                    mysql.connection.commit()
                    print("✅ Fixed: Khushi joined Dhruti's team.")
                except Exception as e:
                    print(f"   Error fixing: {e}")
            else:
                print("✅ They are already on the same project ID.")
                # Maybe Judge is missing?
                cur.execute("SELECT FacultyUserID FROM JudgeAssignment WHERE ProjectID = %s", (d_proj[0],))
                judge = cur.fetchone()
                if not judge:
                    print("⚠️ But there is NO JUDGE assigned to this project yet.")
                else:
                    print(f"   And Judge {judge[0]} is assigned.")

if __name__ == "__main__":
    debug_khushi()
