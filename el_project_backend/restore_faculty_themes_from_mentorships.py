from your_app import create_app, mysql

app = create_app()

def restore_themes_from_mentorships():
    with app.app_context():
        cur = mysql.connection.cursor()
        print("🔧 Restoring Faculty Themes based on Active Mentorships...")
        
        try:
            # 1. Find implied themes from Mentor Assignments
            # Strategy: If a faculty mentors a project in Theme X, assign them to Theme X.
            # Handle conflicts: If multiple themes, pick the one with most projects.
            
            cur.execute("""
                SELECT ma.FacultyUserID, p.ThemeID, count(*) as proj_count
                FROM MentorAssignment ma
                JOIN Project p ON ma.ProjectID = p.ProjectID
                WHERE p.ThemeID IS NOT NULL
                GROUP BY ma.FacultyUserID, p.ThemeID
                ORDER BY ma.FacultyUserID, proj_count DESC
            """)
            
            # Map Faculty -> Theme (picking the one with highest count courtesy of ORDER BY)
            assignments = {}
            rows = cur.fetchall()
            
            for fid, tid, count in rows:
                if fid not in assignments:
                    assignments[fid] = tid
            
            print(f"   Found {len(assignments)} faculty with active mentorships.")
            
            # 2. Assign them
            restored_count = 0
            for fid, tid in assignments.items():
                try:
                    cur.execute("""
                        INSERT INTO FacultyTheme (FacultyUserID, ThemeID)
                        VALUES (%s, %s)
                        ON DUPLICATE KEY UPDATE ThemeID = ThemeID
                    """, (fid, tid))
                    restored_count += 1
                except Exception as e:
                    print(f"   ⚠️ Could not assign {fid} to theme {tid}: {e}")
            
            mysql.connection.commit()
            print(f"✅ Successfully restored {restored_count} faculty theme assignments based on their projects.")
            
            # 3. Check for faculty who are still unassigned but have interests (Fallback)
            # If they have no mentorships, we can't infer proper theme, so we leave them unassigned 
            # OR we could try to match interests strings to theme names? 
            # For now, safe approach: only use mentorships.
            
        except Exception as e:
            mysql.connection.rollback()
            print(f"❌ Error restoring themes: {e}")
        finally:
            cur.close()

if __name__ == "__main__":
    restore_themes_from_mentorships()
