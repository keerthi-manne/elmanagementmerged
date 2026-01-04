from your_app import create_app, mysql
import random
import string

app = create_app()

def generate_google_docs_link():
    """Generate a random but realistic-looking Google Docs link"""
    # Generate random document ID (Google Docs IDs are typically 44 characters)
    chars = string.ascii_letters + string.digits + '-_'
    doc_id = ''.join(random.choices(chars, k=44))
    return f"https://docs.google.com/document/d/{doc_id}/edit?usp=sharing"

def generate_github_link(project_num):
    """Generate a GitHub repository link"""
    repo_names = [
        "ai-traffic-system", "blockchain-voting", "smart-home-iot", 
        "secure-chat-app", "stock-predictor", "ecommerce-platform",
        "healthcare-system", "learning-portal", "weather-prediction",
        "social-analytics", "food-delivery", "music-recommender"
    ]
    repo = repo_names[project_num % len(repo_names)]
    return f"https://github.com/rvce-students/{repo}"

def generate_drive_link():
    """Generate a Google Drive link"""
    chars = string.ascii_letters + string.digits + '-_'
    file_id = ''.join(random.choices(chars, k=33))
    return f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

with app.app_context():
    cur = mysql.connection.cursor()
    
    print("🔄 Updating Project Submissions with varied content...\n")
    
    # Get all submissions
    cur.execute("SELECT SubmissionID, ProjectID, SubmissionType FROM ProjectSubmission")
    submissions = cur.fetchall()
    
    updated_count = 0
    
    for sub_id, project_id, sub_type in submissions:
        # Generate varied content based on submission type
        if sub_type == 'Link':
            # Mix of Google Docs, GitHub, and Drive links
            link_type = random.choice(['docs', 'github', 'drive'])
            if link_type == 'docs':
                content = f"Project Documentation: {generate_google_docs_link()}\n\nThis document contains our complete project report, research, and implementation details."
            elif link_type == 'github':
                content = f"GitHub Repository: {generate_github_link(project_id)}\n\nComplete source code, README, and documentation included."
            else:
                content = f"Project Files: {generate_drive_link()}\n\nIncludes presentation, code, and supporting documents."
        
        elif sub_type == 'File':
            filename = f"project_{project_id}_report.pdf"
            content = f"Uploaded file: {filename}\n\nFile size: {random.randint(500, 5000)}KB\nContains: Full project report, code documentation, test results, and screenshots."
        
        else:  # Text
            content = f"""Official submission for Project {project_id}.

Project Overview:
Our team has successfully completed the implementation with the following deliverables:
- Complete source code with documentation
- Testing and validation results
- User guide and technical documentation
- Presentation materials

Key Features Implemented:
{random.randint(5, 12)} major features completed
All test cases passed
Ready for final review

Documentation: {generate_google_docs_link()}
GitHub: {generate_github_link(project_id)}
"""
        
        # Update the submission
        try:
            cur.execute("""
                UPDATE ProjectSubmission 
                SET SubmissionContent = %s 
                WHERE SubmissionID = %s
            """, (content, sub_id))
            updated_count += 1
            print(f"✓ Updated Submission {sub_id} (Project {project_id}, Type: {sub_type})")
        except Exception as e:
            print(f"✗ Error updating Submission {sub_id}: {e}")
    
    mysql.connection.commit()
    
    print(f"\n{'='*60}")
    print(f"✅ Successfully updated {updated_count} submissions!")
    print(f"{'='*60}\n")
    
    # Show sample of updated submissions
    print("Sample of updated submissions:\n")
    cur.execute("""
        SELECT SubmissionID, ProjectID, SubmissionType, 
               SUBSTRING(SubmissionContent, 1, 100) as Preview
        FROM ProjectSubmission 
        LIMIT 5
    """)
    
    for row in cur.fetchall():
        print(f"ID: {row[0]:3d} | Project: {row[1]:2d} | Type: {row[2]:6s}")
        print(f"  Preview: {row[3]}...")
        print()
