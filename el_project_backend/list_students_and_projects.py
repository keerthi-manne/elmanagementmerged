from your_app import create_app, mysql

app = create_app()

def list_students():
    with app.app_context():
        cur = mysql.connection.cursor()
        
        # Join User, TeamMember, Project, Theme
        cur.execute("""
            SELECT u.Name, u.Email, p.Title, t.ThemeName 
            FROM User u
            JOIN TeamMember tm ON u.UserID = tm.UserID
            JOIN Project p ON tm.ProjectID = p.ProjectID
            LEFT JOIN Theme t ON p.ThemeID = t.ThemeID
            WHERE u.Role = 'Student'
            ORDER BY p.Title
        """)
        
        rows = cur.fetchall()
        
        with open("student_credentials_dump.md", "w", encoding="utf-8") as f:
            f.write("# 🎓 Student Credentials & Projects\n\n")
            f.write("| Student Name | Email (Login) | Password | Project Title | Theme |\n")
            f.write("|---|---|---|---|---|\n")
            
            for name, email, project, theme in rows:
                f.write(f"| {name} | `{email}` | `123456` | {project} | {theme or 'N/A'} |\n")
                
            f.write(f"\n**Total Students Assigned:** {len(rows)}\n")
            # Also add a convenient list for copy-paste
            f.write("\n### Quick Copy Emails:\n")
            for _, email, _, _ in rows:
                f.write(f"- `{email}`\n")
        
        print("✅ Credentials saved to student_credentials_dump.md")

if __name__ == "__main__":
    list_students()
