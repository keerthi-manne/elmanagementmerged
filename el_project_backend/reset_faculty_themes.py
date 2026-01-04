from your_app import create_app, mysql

app = create_app()

def reset_assignments():
    with app.app_context():
        cur = mysql.connection.cursor()
        print("🧹 Resetting Faculty Theme Assignments...")
        
        try:
            # 1. Count current assignments
            cur.execute("SELECT COUNT(*) FROM FacultyTheme")
            count = cur.fetchone()[0]
            print(f"   Found {count} assignments to clear.")
            
            # 2. Delete all
            cur.execute("DELETE FROM FacultyTheme")
            mysql.connection.commit()
            print("✅ All faculty theme assignments have been CLEARED.")
            
        except Exception as e:
            mysql.connection.rollback()
            print(f"❌ Error resetting assignments: {e}")
        finally:
            cur.close()

if __name__ == "__main__":
    reset_assignments()
