from your_app import create_app, mysql

app = create_app()

def debug_logic():
    with app.app_context():
        # Hardcoded test values matching verify script
        current_user_id = 2 # Usually Merin
        # Need Merin's ID
        cur = mysql.connection.cursor()
        cur.execute("SELECT UserID FROM User WHERE Email='merinmeleet@rvce.edu.in'")
        current_user_id = cur.fetchone()[0]
        
        # Need Project ID (Judge Assigned)
        cur.execute("SELECT ProjectID FROM JudgeAssignment WHERE FacultyUserID=%s LIMIT 1", (current_user_id,))
        project_id = cur.fetchone()[0]
        
        # Need Student ID (On project)
        cur.execute("SELECT UserID FROM TeamMember WHERE ProjectID=%s LIMIT 1", (project_id,))
        student_user_id = cur.fetchone()[0]
        
        print(f"Testing with: Faculty={current_user_id}, Project={project_id}, Student={student_user_id}")
        
        try:
            # 1. Role Check
            print("1. Checking Role...")
            cur.execute("SELECT 1 FROM judgeassignment WHERE FacultyUserID = %s AND ProjectID = %s", (current_user_id, project_id))
            is_judge = cur.fetchone()
            
            cur.execute("SELECT 1 FROM mentorassignment WHERE FacultyUserID = %s AND ProjectID = %s", (current_user_id, project_id))
            is_mentor = cur.fetchone()
            
            if is_judge: type_ = 'Judge'
            elif is_mentor: type_ = 'Mentor'
            else: 
                print("❌ No Role!")
                return
            print(f"   Role: {type_}")

            # 2. Team Check
            print("2. Checking Team...")
            cur.execute("SELECT 1 FROM teammember tm WHERE tm.UserID = %s AND tm.ProjectID = %s", (student_user_id, project_id))
            if not cur.fetchone():
                print("❌ Student not on team!")
                return
            print("   Student OK.")

            # 3. Insert
            print("3. Inserting...")
            # score_val = 8.0, feedback = 'Debug', phase='Phase1'
            cur.execute("""
                INSERT INTO evaluation (ProjectID, FacultyUserID, EvaluationType, Score, Feedback, Phase, StudentUserID, EvaluatedAt)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            """, (project_id, current_user_id, type_, 8.0, 'Debug Script', 'Phase1', student_user_id))
            
            print("✅ INSERT QUERY SUCCEEDED.")
            mysql.connection.rollback() # Don't actually save, just test logic
            
        except Exception as e:
            print(f"❌ CRASH: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    debug_logic()
