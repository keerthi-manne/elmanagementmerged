from your_app import create_app, mysql

app = create_app()

def fix_duplicates():
    with app.app_context():
        cur = mysql.connection.cursor()
        print("🧹 Cleaning up multiple project assignments...")
        
        # 1. Find students with multiple projects
        cur.execute("""
            SELECT UserID, COUNT(*) as c 
            FROM TeamMember 
            GROUP BY UserID 
            HAVING c > 1
        """)
        multi_users = cur.fetchall()
        
        print(f"   Found {len(multi_users)} students with multiple projects.")
        
        fixed_count = 0
        for uid, count in multi_users:
            # Get all projects for this user
            cur.execute("SELECT ProjectID FROM TeamMember WHERE UserID = %s", (uid,))
            pids = [row[0] for row in cur.fetchall()]
            
            # Strategy: Keep the one with highest ID (usually newest) OR specific ones
            # Let's keep the LAST one added (highest ID usually implies newest / most relevant)
            # OR checking names... let's just keep the last one.
            keep_pid = pids[-1] 
            
            # Remove others
            for pid in pids:
                if pid != keep_pid:
                    try:
                        cur.execute("DELETE FROM TeamMember WHERE UserID=%s AND ProjectID=%s", (uid, pid))
                        fixed_count += 1
                    except Exception as e:
                        print(f"Error deleting {uid} from {pid}: {e}")
            
            print(f"   - User {uid}: Kept Project {keep_pid}, removed {len(pids)-1} others.")
            
        mysql.connection.commit()
        print(f"✅ Removed {fixed_count} duplicate assignments. Every student now has exactly 1 project.")

if __name__ == "__main__":
    fix_duplicates()
