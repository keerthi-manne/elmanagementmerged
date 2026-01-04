from extensions import db
from app import app
import random

app = app()

def complete_population():
    with app.app_context():
        cur = mysql.connection.cursor()
        print("🚀 Completing Data Population (Safe Mode)...")

        # Get Resources
        cur.execute("SELECT ProjectID FROM Project")
        project_ids = [row[0] for row in cur.fetchall()]
        
        cur.execute("SELECT UserID FROM Faculty")
        faculty_ids = [row[0] for row in cur.fetchall()]
        
        cur.execute("SELECT UserID FROM Student")
        student_ids = [row[0] for row in cur.fetchall()]
        
        print(f"Stats: {len(project_ids)} Projects, {len(faculty_ids)} Faculty, {len(student_ids)} Students")

        # 0. Migrations (Ensure columns exist)
        print("\n🔧 Applying migrations...")
        try:
            cur.execute("ALTER TABLE Evaluation ADD COLUMN Phase VARCHAR(50)")
            print("  ✓ Added Phase column")
        except:
            pass
            
        try:
            cur.execute("ALTER TABLE Evaluation ADD COLUMN StudentUserID VARCHAR(20)")
            print("  ✓ Added StudentUserID column")
        except:
            pass
            
        try:
             cur.execute("ALTER TABLE Theme ADD COLUMN MaxMentors INT DEFAULT 5")
        except:
            pass
            
        mysql.connection.commit()

        # 1. Mentors
        print("\n👥 Assigning Mentors...")
        cur.execute("DELETE FROM MentorAssignment") 
        
        for project_id in project_ids:
            num_mentors = random.randint(1, 2)
            mentors = random.sample(faculty_ids, min(num_mentors, len(faculty_ids)))
            for mentor_id in mentors:
                try:
                    # Try without AssignedAt
                    cur.execute("""
                        INSERT INTO MentorAssignment (ProjectID, FacultyUserID) 
                        VALUES (%s, %s)
                    """, (project_id, mentor_id))
                except Exception as e:
                    print(f"  Error Mentor {project_id}: {e}")
        print("  ✓ Mentors done")

        # 2. Judges
        print("\n⚖️ Assigning Judges...")
        cur.execute("DELETE FROM JudgeAssignment")
        
        for project_id in project_ids:
            num_judges = random.randint(1, 2)
            judges = random.sample(faculty_ids, min(num_judges, len(faculty_ids)))
            for judge_id in judges:
                try:
                    cur.execute("""
                        INSERT INTO JudgeAssignment (ProjectID, FacultyUserID) 
                        VALUES (%s, %s)
                    """, (project_id, judge_id))
                except Exception as e:
                    print(f"  Error Judge {project_id}: {e}")
        print("  ✓ Judges done")

        # 3. Submissions
        print("\n📄 Creating Submissions...")
        cur.execute("DELETE FROM ProjectSubmission")
        
        submission_types = ['Link', 'File', 'Text']
        
        for project_id in project_ids:
            cur.execute("SELECT UserID FROM TeamMember WHERE ProjectID = %s", (project_id,))
            team = [row[0] for row in cur.fetchall()]
            
            if team:
                submitter = team[0]
                sType = random.choice(submission_types)
                content = f"Official submission for Project {project_id}. Docs included."
                try:
                    cur.execute("""
                        INSERT INTO ProjectSubmission (ProjectID, UserID, SubmissionType, SubmissionContent) 
                        VALUES (%s, %s, %s, %s)
                    """, (project_id, submitter, sType, content))
                except Exception as e:
                    print(f"  Error Submission {project_id}: {e}")
        print("  ✓ Submissions done")

        # 4. Evaluations
        print("\n📊 Creating Evaluations...")
        cur.execute("DELETE FROM Evaluation")
        phases = ['Phase1', 'Phase2', 'Phase3']
        
        for project_id in project_ids:
            cur.execute("SELECT UserID FROM TeamMember WHERE ProjectID = %s", (project_id,))
            team = [row[0] for row in cur.fetchall()]
            
            if team and faculty_ids:
                evaluator = random.choice(faculty_ids)
                phase = random.choice(phases)
                score = random.randint(6, 10)
                comments = f"Good progress in {phase}."
                
                for student_id in team:
                    # Use Feedback instead of Comments
                    try:
                        cur.execute("""
                            INSERT INTO Evaluation (ProjectID, StudentUserID, FacultyUserID, Phase, Score, Feedback) 
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (project_id, student_id, evaluator, phase, score, comments))
                    except Exception as e:
                         print(f"  Error Eval {project_id}-{student_id}: {e}")

        print("  ✓ Evaluations done")
        
        mysql.connection.commit()
        print("\n✅ Completed Population Update!")

if __name__ == '__main__':
    complete_population()
