from your_app import create_app, mysql

app = create_app()

def assign_students():
    with app.app_context():
        cur = mysql.connection.cursor()
        print("🔧 Assigning Students to Projects...")
        
        try:
            # 1. Get Projects
            cur.execute("SELECT ProjectID, Title FROM Project")
            projects = cur.fetchall()
            
            # 2. Get Students
            cur.execute("SELECT UserID, Name FROM User WHERE Role='Student'")
            students = cur.fetchall()
            
            if not projects:
                print("❌ No projects found.")
                return
            if not students:
                print("❌ No students found.")
                return
                
            print(f"   Found {len(projects)} projects and {len(students)} students.")
            
            # 3. Assign
            assigned_count = 0
            for i, (sid, sname) in enumerate(students):
                # Round robin assignment
                pid, ptitle = projects[i % len(projects)]
                
                try:
                    cur.execute("""
                        INSERT INTO TeamMember (ProjectID, UserID)
                        VALUES (%s, %s)
                    """, (pid, sid))
                    assigned_count += 1
                except:
                    pass # Ignore if already assigned
            
            mysql.connection.commit()
            print(f"✅ Assigned {assigned_count} students to projects.")
            
        except Exception as e:
            mysql.connection.rollback()
            print(f"❌ Error: {e}")
        finally:
            cur.close()

if __name__ == "__main__":
    assign_students()
