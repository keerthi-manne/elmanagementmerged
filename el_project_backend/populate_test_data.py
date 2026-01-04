from your_app import create_app, mysql
from your_app.auth.utils import hash_password
import random
from datetime import datetime, timedelta

app = create_app()

def populate():
    with app.app_context():
        cur = mysql.connection.cursor()
        print("🚀 Starting Data Population...")

        # 0. Ensure Schema is up to date (Migration)
        print("🔧 Applying migrations...")
        try:
            cur.execute("ALTER TABLE Faculty ADD COLUMN Interests TEXT")
        except:
            pass # Column likely exists
            
        try:
            cur.execute("ALTER TABLE Theme ADD COLUMN MaxMentors INT DEFAULT 5")
        except:
            pass
            
        try:
            cur.execute("ALTER TABLE Theme ADD COLUMN MaxJudges INT DEFAULT 5")
        except:
            pass
            
        try:
            cur.execute("ALTER TABLE Evaluation ADD COLUMN Phase VARCHAR(50)")
        except:
            pass
            
        try:
            cur.execute("ALTER TABLE Evaluation ADD COLUMN StudentUserID VARCHAR(20)")
        except:
            pass
            
        mysql.connection.commit()

        # 1. Clear existing demo data (optional, but cleaner)
        # Be careful not to delete Admin if they want to keep it. 
        # For now, let's just INSERT IGNORE or handle duplicates.
        
        # --- THEMES ---
        themes = [
            ("Machine Learning", "Projects involving AI, Deep Learning, and Neural Networks"),
            ("Blockchain", "Crypto, Smart Contracts, and Decentralized Apps"),
            ("IoT & Embedded", "Internet of Things, Arduino, Raspberry Pi"),
            ("Web Security", "Cybersecurity, Encryption, and Network Defense"),
            ("Cloud Computing", "AWS, Azure, Microservices")
        ]
        
        print(f"📦 Seeding {len(themes)} Themes...")
        for name, desc in themes:
            cur.execute("""
                INSERT INTO Theme (ThemeName, Description) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE Description=VALUES(Description)
            """, (name, desc))
        mysql.connection.commit()
        
        # Get Theme IDs
        cur.execute("SELECT ThemeID, ThemeName FROM Theme")
        theme_map = {row[1]: row[0] for row in cur.fetchall()}

        # --- FACULTY (With Interests for Auto-Assign) ---
        faculty_data = [
            ("FAC001", "Dr. Alan Turing", "alan@rvce.edu.in", "CSE", "Artificial Intelligence, Deep Learning, Neural Networks"),
            ("FAC002", "Dr. Grace Hopper", "grace@rvce.edu.in", "ISE", "Compiler Design, Programming Languages, Web Development"),
            ("FAC003", "Prof. Satoshi", "satoshi@rvce.edu.in", "CSE", "Blockchain, Cryptography, Distributed Systems"),
            ("FAC004", "Prof. Shannon", "shannon@rvce.edu.in", "ECE", "Communication, IoT, Signal Processing"),
            ("FAC005", "Dr. Alice", "alice@rvce.edu.in", "ISE", "Network Security, Cyber Defense, Ethical Hacking")
        ]
        
        print(f"👨‍🏫 Seeding {len(faculty_data)} Faculty...")
        password = hash_password("faculty123")
        for fid, name, email, dept, interests in faculty_data:
            # Create User
            cur.execute("""
                INSERT INTO User (UserID, Name, Email, PasswordHash, Role, Status)
                VALUES (%s, %s, %s, %s, 'Faculty', 'Approved')
                ON DUPLICATE KEY UPDATE Name=VALUES(Name)
            """, (fid, name, email, password))
            
            # Create Faculty Profile
            cur.execute("""
                INSERT INTO Faculty (UserID, Dept, Interests)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE Interests=VALUES(Interests)
            """, (fid, dept, interests))
        mysql.connection.commit()

        # --- STUDENTS ---
        students_data = []
        for i in range(1, 21):
            sid = f"1RV23CS{i:03d}"
            name = f"Student {i}"
            email = f"student{i}@rvce.edu.in"
            students_data.append((sid, name, email))
            
        print(f"🎓 Seeding {len(students_data)} Students...")
        st_password = hash_password("student123")
        for sid, name, email in students_data:
            cur.execute("""
                INSERT INTO User (UserID, Name, Email, PasswordHash, Role, Status)
                VALUES (%s, %s, %s, %s, 'Student', 'Approved')
                ON DUPLICATE KEY UPDATE Name=VALUES(Name)
            """, (sid, name, email, st_password))
            
            cur.execute("""
                INSERT INTO Student (UserID, Dept, Semester)
                VALUES (%s, 'CSE', 5)
                ON DUPLICATE KEY UPDATE Semester=5
            """, (sid,))
        mysql.connection.commit()

        # --- PROJECTS & TEAMS ---
        # We will create 5 projects with consistent data
        projects = [
            ("AI Traffic Control", "Using Computer Vision to manage city traffic lights.", "Traffic congestion is a major issue...", "Machine Learning", ["1RV23CS001", "1RV23CS002", "1RV23CS003"]),
            ("Decentralized Voting", "A blockchain-based voting system for transparency.", "Elections need trust...", "Blockchain", ["1RV23CS004", "1RV23CS005"]),
            ("Smart Irrigation", "IoT sensors for automated farm watering.", "Water scarcity requires smart usage...", "IoT & Embedded", ["1RV23CS006", "1RV23CS007", "1RV23CS008"]),
            ("Secure Chat App", "End-to-end encrypted messaging platform.", "Privacy is eroding...", "Web Security", ["1RV23CS009", "1RV23CS010"]),
            ("Stock Predictor", "LSTM models to predict stock trends.", "Financial markets are volatile...", "Machine Learning", ["1RV23CS011", "1RV23CS012"])
        ]
        
        print(f"🚀 Seeding {len(projects)} Projects & Assignments...")
        for title, abstract, problem, theme_name, members in projects:
            if theme_name not in theme_map:
                continue
            theme_id = theme_map[theme_name]
            
            # Create Project
            cur.execute("""
                INSERT INTO Project (Title, Abstract, ProblemStatement, ThemeID, Status)
                VALUES (%s, %s, %s, %s, 'Approved')
            """, (title, abstract, problem, theme_id))
            project_id = cur.lastrowid
            
            # Add Team Members
            for member_id in members:
                try:
                    cur.execute("INSERT INTO TeamMember (ProjectID, UserID) VALUES (%s, %s)", (project_id, member_id))
                except:
                    pass # Skip if already in team
            
            # Add Submission (For Plagiarism Test)
            # Make one submission slightly plagiarized from another for testing
            content = f"This is the detailed report for {title}. {abstract} " + "We used Python and JavaScript to build this system. The results were promising."
            if "Voting" in title:
                # Plagiarism trap: Reuse content from Traffic Control
                content = "Using Computer Vision to manage city traffic lights. Traffic congestion is a major issue. We used Python and JavaScript."
            
            # Using the first student in the team as the submitter
            submitter_id = members[0]
            
            try:
                cur.execute("""
                    INSERT INTO projectsubmission (ProjectID, UserID, SubmissionType, SubmissionContent, SubmittedAt)
                    VALUES (%s, %s, 'Link', %s, NOW())
                """, (project_id, submitter_id, content))
            except Exception as e:
                print(f"⚠️ Submission insert failed: {e}")
            
            # Add Evaluation (For Data Analysis)
            # Random score between 6 and 10
            score = random.randint(6, 10)
            try:
                cur.execute("""
                    INSERT INTO evaluation (ProjectID, StudentUserID, FacultyUserID, Phase, Score, Comments, EvaluatedAt)
                    VALUES (%s, %s, 'FAC001', 'Phase 1', %s, 'Good work!', NOW())
                """, (project_id, members[0], score))
            except Exception as e:
                print(f"⚠️ Evaluation insert failed: {e}")

        # --- ADMIN (Ensure at least one exists) ---
        print("👮 Seeding Admin User...")
        admin_pass = hash_password("admin123")
        try:
            cur.execute("""
                INSERT INTO User (UserID, Name, Email, PasswordHash, Role, Status)
                VALUES ('ADMIN001', 'System Admin', 'admin@rvce.edu.in', %s, 'Admin', 'Approved')
                ON DUPLICATE KEY UPDATE Role='Admin'
            """, (admin_pass,))
            
            # Ensure in Coordinator table (if that's where admins live)
            cur.execute("""
                INSERT INTO Coordinator (UserID, Dept)
                VALUES ('ADMIN001', 'CSE')
                ON DUPLICATE KEY UPDATE Dept='CSE'
            """)
        except Exception as e:
            print(f"⚠️ Admin create failed: {e}")

        mysql.connection.commit()
        print("✅ Data Population Complete! Login as Admin to check.")

if __name__ == '__main__':
    populate()
