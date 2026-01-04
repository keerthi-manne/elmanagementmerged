from your_app import create_app, mysql

app = create_app()

# The Google Docs link to use for all submissions
SUBMISSION_LINK = "https://docs.google.com/document/d/1kTixTIJgZcnrQ2S6ZuRzyzonY3UTSQGe1WVKwwE2qtU/edit?usp=sharing"

with app.app_context():
    cur = mysql.connection.cursor()
    
    print("🔄 Updating all Project Submissions with the same Google Docs link...\n")
    
    # Get all submissions
    cur.execute("SELECT SubmissionID, ProjectID, SubmissionType FROM ProjectSubmission")
    submissions = cur.fetchall()
    
    updated_count = 0
    
    for sub_id, project_id, sub_type in submissions:
        # Set content with the same link for all submissions
        content = f"""Project Submission Documentation

Link: {SUBMISSION_LINK}

This document contains:
- Complete project report and documentation
- Source code details and implementation
- Testing and validation results
- Screenshots and demo materials
"""
        
        # Update the submission
        try:
            cur.execute("""
                UPDATE ProjectSubmission 
                SET SubmissionContent = %s 
                WHERE SubmissionID = %s
            """, (content, sub_id))
            updated_count += 1
            print(f"✓ Updated Submission {sub_id} (Project {project_id})")
        except Exception as e:
            print(f"✗ Error updating Submission {sub_id}: {e}")
    
    mysql.connection.commit()
    
    print(f"\n{'='*60}")
    print(f"✅ Successfully updated {updated_count} submissions!")
    print(f"All submissions now use: {SUBMISSION_LINK}")
    print(f"{'='*60}\n")
    
    # Verify the update
    print("Verification - showing first 3 submissions:\n")
    cur.execute("""
        SELECT SubmissionID, ProjectID, SubmissionContent
        FROM ProjectSubmission 
        LIMIT 3
    """)
    
    for row in cur.fetchall():
        print(f"Submission {row[0]} (Project {row[1]}):")
        print(f"{row[2]}\n")
