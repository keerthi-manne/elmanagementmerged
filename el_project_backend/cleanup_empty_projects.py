from your_app import create_app, mysql

app = create_app()

def cleanup_projects():
    with app.app_context():
        cur = mysql.connection.cursor()
        print("🧹 Finding empty projects...")
        
        # 1. Find Projects with NO TeamMembers
        # Left Join Project -> TeamMember
        cur.execute("""
            SELECT p.ProjectID, p.Title 
            FROM Project p
            LEFT JOIN TeamMember tm ON p.ProjectID = tm.ProjectID
            WHERE tm.UserID IS NULL
        """)
        empty_projects = cur.fetchall()
        
        print(f"   Found {len(empty_projects)} empty projects:")
        for pid, title in empty_projects:
            print(f"    - ID {pid}: {title}")
            
        if not empty_projects:
            print("✅ No empty projects found.")
            return

        print(f"\n🗑️ Deleting {len(empty_projects)} projects and their dependencies...")
        
        pids = [p[0] for p in empty_projects]
        placeholders = ', '.join(['%s'] * len(pids))
        
        # Delete Dependencies
        tables = ['JudgeAssignment', 'MentorAssignment', 'ProjectSubmission', 'Evaluation', 'Notification']
        for table in tables:
            try:
                # Check if ProjectID column exists? Yes usually.
                # Notification might handle ProjectID? need check schema. 
                # Assuming yes for Assignments/Submissions/Evals.
                if table == 'Notification':
                    # Try to delete by ProjectID if exists, else ignore specific error
                    pass
                    
                cur.execute(f"DELETE FROM {table} WHERE ProjectID IN ({placeholders})", pids)
                print(f"   - Cleared {table}.")
            except Exception as e:
                print(f"   ⚠️ Error clearing {table}: {e}")

        # FORCE DELETE
        try:
            cur.execute("SET FOREIGN_KEY_CHECKS=0")
            
            # Delete Projects
            cur.execute(f"DELETE FROM Project WHERE ProjectID IN ({placeholders})", pids)
            
            # Also try to clean dependencies again to minimize orphans
            for table in tables:
                try:
                    cur.execute(f"DELETE FROM {table} WHERE ProjectID IN ({placeholders})", pids)
                except:
                    pass
            
            cur.execute("SET FOREIGN_KEY_CHECKS=1")
            mysql.connection.commit()
            print(f"✅ FORCE DELETED {len(pids)} empty projects.")
        except Exception as e:
            print(f"❌ Error deleting projects: {e}")
            cur.execute("SET FOREIGN_KEY_CHECKS=1")
            mysql.connection.rollback()

if __name__ == "__main__":
    cleanup_projects()
