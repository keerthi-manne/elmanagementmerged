from your_app import create_app, mysql

app = create_app()

def reset_transactional_data():
    with app.app_context():
        cur = mysql.connection.cursor()
        print("🧹 Cleaning Transactional Data (Keeping Users & Projects)...")
        
        tables_to_clear = [
            'Notification',
            'Evaluation',
            'ProjectSubmission',
            'JudgeAssignment',
            'MentorAssignment',
            'FacultyTheme'
        ]
        
        for table in tables_to_clear:
            try:
                cur.execute(f"DELETE FROM {table}")
                print(f"  ✓ Cleared {table}")
            except Exception as e:
                print(f"  ❌ Error clearing {table}: {e}")
                
        mysql.connection.commit()
        print("\n✅ Data Reset Complete!")
        print("   - Users, Faculties, Students: PRESERVED")
        print("   - Themes, Projects, Teams: PRESERVED")
        print("   - Assignments, Submissions, Evaluations: CLEARED (Ready for manual flow)")

if __name__ == "__main__":
    reset_transactional_data()
