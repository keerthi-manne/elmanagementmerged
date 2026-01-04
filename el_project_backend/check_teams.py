from extensions import db
from models import Student, Team, TeamMember, Project, Faculty, Course

app = create_app()
with app.app_context():
    cur = mysql.connection.cursor()
    
    print("\n========== TEAM ASSIGNMENTS ==========\n")
    
    # Check students without projects
    cur.execute("""
        SELECT U.UserID, U.Name, U.Email 
        FROM User U 
        WHERE U.Role='Student' 
        AND U.UserID NOT IN (SELECT UserID FROM TeamMember)
    """)
    unassigned = cur.fetchall()
    
    if unassigned:
        print(f"Students WITHOUT projects: {len(unassigned)}")
        for row in unassigned:
            print(f"  - {row[0]}: {row[1]} ({row[2]})")
    else:
        print("All students are assigned to projects!")
    
    # Check projects without teams
    cur.execute("""
        SELECT P.ProjectID, P.Title 
        FROM Project P 
        WHERE P.ProjectID NOT IN (SELECT ProjectID FROM TeamMember)
    """)
    no_team = cur.fetchall()
    
    if no_team:
        print(f"\nProjects WITHOUT teams: {len(no_team)}")
        for row in no_team:
            print(f"  - Project {row[0]}: {row[1]}")
    else:
        print("\nAll projects have at least one team member!")
    
    # Show project-team mapping
    print("\n========== PROJECT-TEAM MAPPING ==========\n")
    cur.execute("""
        SELECT P.ProjectID, P.Title, 
               COUNT(TM.UserID) as TeamSize,
               GROUP_CONCAT(U.Name SEPARATOR ', ') as TeamMembers
        FROM Project P
        LEFT JOIN TeamMember TM ON P.ProjectID = TM.ProjectID
        LEFT JOIN User U ON TM.UserID = U.UserID
        GROUP BY P.ProjectID, P.Title
        ORDER BY P.ProjectID
    """)
    
    projects = cur.fetchall()
    for row in projects:
        team_size = row[2] if row[2] else 0
        members = row[3] if row[3] else "No members"
        print(f"Project {row[0]:2d}: {row[1][:35]:35s} | Team: {team_size} | Members: {members}")
    
    print("\n======================================\n")
