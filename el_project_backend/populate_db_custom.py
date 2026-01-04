from your_app import create_app
from extensions import db
from your_app.auth.utils import hash_password
import random
from datetime import datetime, timedelta

app = create_app()

def populate():
    with app.app_context():
        cur = mysql.connection.cursor()
        print("🚀 Starting Custom Data Population...")

        # Password for all users
        password = hash_password("123456")

        # 0. Clear existing data (except schema)
        print("🧹 Clearing existing data...")
        tables_to_clear = [
            'Evaluation', 'ProjectSubmission', 'TeamMember', 'MentorAssignment', 
            'JudgeAssignment', 'Notification', 'Project', 'Student', 'Faculty', 
            'Coordinator', 'User', 'Theme'
        ]
        
        for table in tables_to_clear:
            try:
                cur.execute(f"DELETE FROM {table}")
                print(f"  ✓ Cleared {table}")
            except Exception as e:
                print(f"  ⚠️ Could not clear {table}: {e}")
        
        mysql.connection.commit()

        # 1. Create Admin
        print("👮 Creating Admin...")
        try:
            cur.execute("""
                INSERT INTO User (UserID, Name, Email, PasswordHash, Role, Status)
                VALUES ('ADMIN001', 'System Admin', 'admin@rvce.edu.in', %s, 'Admin', 'Approved')
            """, (password,))
            
            cur.execute("""
                INSERT INTO Coordinator (UserID, Dept)
                VALUES ('ADMIN001', 'CSE')
            """)
            print("  ✓ Admin created: admin@rvce.edu.in / 123456")
        except Exception as e:
            print(f"  ⚠️ Admin creation error: {e}")
        
        mysql.connection.commit()

        # 2. Create Faculty
        print("👨‍🏫 Creating 10 Faculty...")
        faculty_names = ['merinmeleet', 'anala', 'mamtha', 'raghavendra', 'sushmita', 
                        'poornima', 'srinivas', 'kavitha', 'gangadhar', 'ashwini']
        departments = ['CSE', 'ISE', 'ECE', 'CSE', 'ISE', 'CSE', 'ECE', 'ISE', 'CSE', 'ISE']
        interests_list = [
            'Machine Learning, AI, Neural Networks',
            'Blockchain, Cryptography, Distributed Systems',
            'IoT, Embedded Systems, Robotics',
            'Web Development, Full Stack, Cloud',
            'Cybersecurity, Network Security, Ethical Hacking',
            'Data Science, Big Data, Analytics',
            'Mobile Development, App Design, UX',
            'Database Systems, SQL, NoSQL',
            'Computer Vision, Image Processing',
            'Software Engineering, DevOps, Agile'
        ]
        
        for i, name in enumerate(faculty_names):
            fac_id = f"facrv{123 + i}"
            email = f"{name}@rvce.edu.in"
            dept = departments[i]
            interests = interests_list[i]
            
            try:
                cur.execute("""
                    INSERT INTO User (UserID, Name, Email, PasswordHash, Role, Status)
                    VALUES (%s, %s, %s, %s, 'Faculty', 'Approved')
                """, (fac_id, name.capitalize(), email, password))
                
                cur.execute("""
                    INSERT INTO Faculty (UserID, Dept, Interests)
                    VALUES (%s, %s, %s)
                """, (fac_id, dept, interests))
                
                print(f"  ✓ Faculty: {email} / {fac_id}")
            except Exception as e:
                print(f"  ⚠️ Faculty creation error for {name}: {e}")
        
        mysql.connection.commit()

        # 3. Create Students
        print("🎓 Creating 10 Students...")
        student_names = ['keerthi', 'bhavya', 'divya', 'khushi', 'mahika', 
                        'kavya', 'dhruti', 'ganashree', 'aishwarya', 'arunima']
        branches = ['is', 'cs', 'ec', 'is', 'cs', 'is', 'cs', 'ec', 'is', 'cs']
        
        for i, name in enumerate(student_names):
            student_id = f"1RV23{branches[i].upper()}{(i+1):03d}"
            email = f"{name}{branches[i][0]}.{branches[i]}23@rvce.edu.in"
            dept_map = {'is': 'ISE', 'cs': 'CSE', 'ec': 'ECE'}
            dept = dept_map[branches[i]]
            
            try:
                cur.execute("""
                    INSERT INTO User (UserID, Name, Email, PasswordHash, Role, Status)
                    VALUES (%s, %s, %s, %s, 'Student', 'Approved')
                """, (student_id, name.capitalize(), email, password))
                
                cur.execute("""
                    INSERT INTO Student (UserID, Dept, Semester)
                    VALUES (%s, %s, 5)
                """, (student_id, dept))
                
                print(f"  ✓ Student: {email} / {student_id}")
            except Exception as e:
                print(f"  ⚠️ Student creation error for {name}: {e}")
        
        mysql.connection.commit()

        # 4. Create Themes
        print("🎨 Creating 10+ Themes...")
        themes = [
            ("Machine Learning", "AI, Deep Learning, Neural Networks, Computer Vision"),
            ("Blockchain", "Cryptocurrency, Smart Contracts, Decentralized Applications"),
            ("IoT & Embedded", "Internet of Things, Arduino, Raspberry Pi, Sensors"),
            ("Web Security", "Cybersecurity, Encryption, Network Defense, Ethical Hacking"),
            ("Cloud Computing", "AWS, Azure, Microservices, Serverless Architecture"),
            ("Mobile Development", "Android, iOS, React Native, Flutter"),
            ("Data Science", "Big Data, Analytics, Data Mining, Visualization"),
            ("Web Development", "Full Stack, Frontend, Backend, APIs"),
            ("Game Development", "Unity, Unreal Engine, Game Design, Graphics"),
            ("Robotics", "Automation, ROS, Autonomous Systems, AI Robots"),
            ("AR/VR", "Augmented Reality, Virtual Reality, Mixed Reality"),
            ("Quantum Computing", "Quantum Algorithms, Quantum Cryptography")
        ]
        
        theme_ids = []
        for name, desc in themes:
            try:
                cur.execute("""
                    INSERT INTO Theme (ThemeName, Description, MaxMentors, MaxJudges)
                    VALUES (%s, %s, 5, 5)
                """, (name, desc))
                theme_ids.append(cur.lastrowid)
                print(f"  ✓ Theme: {name}")
            except Exception as e:
                print(f"  ⚠️ Theme creation error for {name}: {e}")
        
        mysql.connection.commit()

        # Get all theme IDs
        cur.execute("SELECT ThemeID FROM Theme")
        theme_ids = [row[0] for row in cur.fetchall()]

        # Get all student IDs
        cur.execute("SELECT UserID FROM Student")
        student_ids = [row[0] for row in cur.fetchall()]

        # Get all faculty IDs
        cur.execute("SELECT UserID FROM Faculty")
        faculty_ids = [row[0] for row in cur.fetchall()]

        # 5. Create Projects (at least 10)
        print("🚀 Creating 10+ Projects...")
        project_titles = [
            "AI Traffic Management System",
            "Blockchain Voting Platform",
            "Smart Home Automation",
            "Secure Chat Application",
            "Stock Price Predictor",
            "E-Commerce Platform",
            "Healthcare Management System",
            "Online Learning Portal",
            "Weather Prediction System",
            "Social Media Analytics Tool",
            "Food Delivery App",
            "Music Recommendation Engine"
        ]
        
        project_ids = []
        for i, title in enumerate(project_titles):
            theme_id = theme_ids[i % len(theme_ids)]
            abstract = f"This project focuses on {title.lower()} using modern technologies and innovative approaches."
            problem_stmt = f"The problem we are addressing is the lack of efficient {title.lower()} solutions in the current market."
            
            try:
                cur.execute("""
                    INSERT INTO Project (Title, Abstract, ProblemStatement, ThemeID, Status, CreatedAt)
                    VALUES (%s, %s, %s, %s, 'Approved', NOW())
                """, (title, abstract, problem_stmt, theme_id))
                project_id = cur.lastrowid
                project_ids.append(project_id)
                print(f"  ✓ Project: {title}")
                
                # Add team members (1-3 students per project)
                num_members = random.randint(1, 3)
                team_students = random.sample(student_ids, min(num_members, len(student_ids)))
                
                for student_id in team_students:
                    try:
                        cur.execute("""
                            INSERT INTO TeamMember (ProjectID, UserID)
                            VALUES (%s, %s)
                        """, (project_id, student_id))
                        print(f"    - Added {student_id} to team")
                    except Exception as e:
                        print(f"    ⚠️ TeamMember error for {student_id}: {e}")
                
            except Exception as e:
                print(f"  ⚠️ Project creation error for {title}: {e}")
        
        mysql.connection.commit()

        # 6. Assign Mentors to Projects
        print("👥 Assigning Mentors to Projects...")
        for project_id in project_ids:
            # Assign 1-2 mentors per project
            num_mentors = random.randint(1, 2)
            mentors = random.sample(faculty_ids, min(num_mentors, len(faculty_ids)))
            
            for mentor_id in mentors:
                try:
                    cur.execute("""
                        INSERT INTO MentorAssignment (ProjectID, FacultyUserID, AssignedAt)
                        VALUES (%s, %s, NOW())
                    """, (project_id, mentor_id))
                except:
                    pass  # Ignore duplicates
        
        mysql.connection.commit()

        # 7. Assign Judges to Projects
        print("⚖️ Assigning Judges to Projects...")
        for project_id in project_ids:
            # Assign 1-2 judges per project
            num_judges = random.randint(1, 2)
            judges = random.sample(faculty_ids, min(num_judges, len(faculty_ids)))
            
            for judge_id in judges:
                try:
                    cur.execute("""
                        INSERT INTO JudgeAssignment (ProjectID, FacultyUserID, AssignedAt)
                        VALUES (%s, %s, NOW())
                    """, (project_id, judge_id))
                except:
                    pass  # Ignore duplicates
        
        mysql.connection.commit()

        # 8. Create Project Submissions (at least 10)
        print("📄 Creating Project Submissions...")
        submission_types = ['Link', 'File', 'Text']
        
        for project_id in project_ids:
            # Get team members for this project
            cur.execute("SELECT UserID FROM TeamMember WHERE ProjectID = %s", (project_id,))
            team = [row[0] for row in cur.fetchall()]
            
            if team:
                submitter = team[0]  # First team member submits
                submission_type = random.choice(submission_types)
                content = f"Submission content for project {project_id}. This is a detailed report with code and documentation."
                
                try:
                    cur.execute("""
                        INSERT INTO ProjectSubmission (ProjectID, UserID, SubmissionType, SubmissionContent, SubmittedAt)
                        VALUES (%s, %s, %s, %s, NOW())
                    """, (project_id, submitter, submission_type, content))
                    print(f"  ✓ Submission for Project {project_id}")
                except Exception as e:
                    print(f"  ⚠️ Submission error for project {project_id}: {e}")
        
        mysql.connection.commit()

        # 9. Create Evaluations (at least 10)
        print("📊 Creating Evaluations...")
        phases = ['Phase 1', 'Phase 2', 'Phase 3', 'Final']
        
        for project_id in project_ids:
            # Get team members
            cur.execute("SELECT UserID FROM TeamMember WHERE ProjectID = %s", (project_id,))
            team = [row[0] for row in cur.fetchall()]
            
            # Get a faculty evaluator
            if faculty_ids and team:
                evaluator = random.choice(faculty_ids)
                phase = random.choice(phases)
                score = random.randint(6, 10)
                comments = f"Good work on phase {phase}. Score: {score}/10"
                
                for student_id in team:
                    try:
                        cur.execute("""
                            INSERT INTO Evaluation (ProjectID, StudentUserID, FacultyUserID, Phase, Score, Comments, EvaluatedAt)
                            VALUES (%s, %s, %s, %s, %s, %s, NOW())
                        """, (project_id, student_id, evaluator, phase, score, comments))
                    except Exception as e:
                        print(f"  ⚠️ Evaluation error: {e}")
        
        mysql.connection.commit()

        # 10. Create Notifications (at least 10)
        print("🔔 Creating Notifications...")
        notification_messages = [
            "Your project has been approved!",
            "New mentor assigned to your project.",
            "Submission deadline is approaching.",
            "Evaluation completed for your project.",
            "Judge assigned for final evaluation.",
            "Project presentation scheduled.",
            "Feedback available for your submission.",
            "Team invitation accepted.",
            "Project status updated.",
            "New announcement from admin."
        ]
        
        notification_types = ['info', 'success', 'warning', 'error']
        all_users = student_ids + faculty_ids + ['ADMIN001']
        
        for i, message in enumerate(notification_messages):
            user = all_users[i % len(all_users)]
            notif_type = notification_types[i % len(notification_types)]
            
            try:
                cur.execute("""
                    INSERT INTO Notification (UserID, Message, Type, Status, Timestamp)
                    VALUES (%s, %s, %s, 'Unread', NOW())
                """, (user, message, notif_type))
            except Exception as e:
                print(f"  ⚠️ Notification error: {e}")
        
        mysql.connection.commit()

        # Final Summary
        print("\n" + "="*60)
        print("✅ DATABASE POPULATION COMPLETE!")
        print("="*60)
        
        # Count records in each table
        tables_to_count = [
            'User', 'Student', 'Faculty', 'Coordinator', 'Theme', 
            'Project', 'TeamMember', 'MentorAssignment', 'JudgeAssignment',
            'ProjectSubmission', 'Evaluation', 'Notification'
        ]
        
        print("\n📊 RECORD COUNTS:")
        for table in tables_to_count:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                count = cur.fetchone()[0]
                print(f"  {table:20s}: {count:3d} rows")
            except:
                pass
        
        print("\n🔐 LOGIN CREDENTIALS:")
        print("  Admin:   admin@rvce.edu.in / 123456")
        print("  Faculty: <name>@rvce.edu.in / 123456")
        print("  Student: <name><branch_initial>.<branch>23@rvce.edu.in / 123456")
        print("  Example: keerthii.is23@rvce.edu.in / 123456")
        print("="*60 + "\n")

if __name__ == '__main__':
    populate()
