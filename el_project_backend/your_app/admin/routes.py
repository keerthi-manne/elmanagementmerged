from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from your_app import mysql
from your_app.auth.routes import roles_required

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/assign_faculty_theme', methods=['POST'])
@jwt_required()
@roles_required('Admin')
def assign_faculty_theme():
    data = request.json or {}
    faculty_user_id = data.get('FacultyUserID')
    theme_id = data.get('ThemeID')

    if not faculty_user_id or not theme_id:
        return jsonify({'error': 'FacultyUserID and ThemeID are required'}), 400

    cur = mysql.connection.cursor()
    try:
        # Optional: ensure user exists and is Faculty
        cur.execute("SELECT Role FROM user WHERE UserID = %s", (faculty_user_id,))
        row = cur.fetchone()
        if not row:
            return jsonify({'error': 'User not found'}), 404
        if row[0] != 'Faculty':
            return jsonify({'error': 'User is not a faculty member'}), 400

        # Optional: ensure theme exists
        cur.execute("SELECT 1 FROM Theme WHERE ThemeID = %s", (theme_id,))
        if not cur.fetchone():
            return jsonify({'error': 'Theme not found'}), 404

        # Upsert: one theme per faculty (FacultyUserID is PK in FacultyTheme)
        cur.execute("""
            INSERT INTO FacultyTheme (FacultyUserID, ThemeID)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE ThemeID = VALUES(ThemeID)
        """, (faculty_user_id, theme_id))

        mysql.connection.commit()
        return jsonify({'message': 'Faculty assigned to theme successfully'}), 200
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
@admin_bp.route('/faculty_theme_assignments', methods=['GET'])
@jwt_required()
@roles_required('Admin')
def get_faculty_theme_assignments():
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            SELECT ft.FacultyUserID, u.Name, ft.ThemeID, t.ThemeName
            FROM FacultyTheme ft
            JOIN user u ON ft.FacultyUserID = u.UserID
            JOIN theme t ON ft.ThemeID = t.ThemeID
            ORDER BY u.Name, t.ThemeName
        """)
        rows = cur.fetchall()
        data = []
        for r in rows:
            data.append({
                'FacultyUserID': r[0],
                'FacultyName': r[1],
                'ThemeID': r[2],
                'ThemeName': r[3]
            })
        return jsonify({'assignments': data}), 200
    finally:
        cur.close()
@admin_bp.route('/projects_pending_approval', methods=['GET'])
@jwt_required()
@roles_required('Admin')
def get_projects_pending_approval():
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            SELECT p.ProjectID, p.Title, p.Abstract, p.ProblemStatement, p.Status,
                   p.ThemeID, t.ThemeName,
                   COUNT(DISTINCT tm.UserID) as team_size,
                   GROUP_CONCAT(DISTINCT u.Name SEPARATOR ', ') as team_members
            FROM Project p
            LEFT JOIN Theme t ON p.ThemeID = t.ThemeID
            LEFT JOIN TeamMember tm ON p.ProjectID = tm.ProjectID
            LEFT JOIN User u ON tm.UserID = u.UserID
            WHERE p.Status IN ('Unassigned', 'Pending', 'Submitted')
            GROUP BY p.ProjectID, p.Title, p.Abstract, p.ProblemStatement, p.Status, p.ThemeID, t.ThemeName
            ORDER BY p.ProjectID DESC
        """)
        rows = cur.fetchall()

        projects = []
        for row in rows:
            projects.append({
                'ProjectID': row[0],
                'Title': row[1] or f'Project {row[0]}',
                'Abstract': row[2] or '',
                'ProblemStatement': row[3] or '',
                'Status': row[4],
                'ThemeID': row[5],
                'ThemeName': row[6] or 'Unknown',
                'TeamSize': row[7] or 0,
                'TeamMembers': row[8] or ''
            })

        return jsonify({'projects': projects}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()

# ✅ NEW: NLP-Based Auto-Assignment with TF-IDF Similarity
@admin_bp.route('/auto_assign', methods=['POST'])
@jwt_required()
@roles_required('Admin')
def auto_assign_faculty():
    """
    🤖 AI-Powered Auto-Assignment using NLP
    
    Features:
    - TF-IDF text similarity for semantic matching
    - Synonym expansion (ML = Machine Learning)
    - Constraint solving (capacity limits)
    - Load balancing algorithm
    - Transaction-based execution
    """
    import re
    from collections import Counter
    import math
    
    cur = mysql.connection.cursor()
    try:
        # 1. Get all unassigned faculty with interests
        cur.execute("""
            SELECT f.UserID, f.Interests, u.Name
            FROM Faculty f
            JOIN User u ON f.UserID = u.UserID
            LEFT JOIN FacultyTheme ft ON f.UserID = ft.FacultyUserID
            WHERE ft.FacultyUserID IS NULL
            AND f.Interests IS NOT NULL
            AND f.Interests != ''
        """)
        unassigned_faculty = cur.fetchall()
        
        if not unassigned_faculty:
            return jsonify({'message': 'No unassigned faculty with interests found', 'assignments': []}), 200
        
        # 2. Get all themes with current counts
        cur.execute("""
            SELECT t.ThemeID, t.ThemeName, t.Description, 
                   COALESCE(t.MaxMentors, 5) as MaxMentors,
                   COUNT(ft.FacultyUserID) as CurrentCount
            FROM Theme t
            LEFT JOIN FacultyTheme ft ON t.ThemeID = ft.ThemeID
            GROUP BY t.ThemeID, t.ThemeName, t.Description, t.MaxMentors
        """)
        themes = cur.fetchall()
        
        # 3. 🧠 NLP Processing Functions
        def normalize_text(text):
            """Lowercase, remove special chars, tokenize"""
            if not text:
                return []
            text = text.lower()
            text = re.sub(r'[^a-z0-9\s]', '', text)
            tokens = text.split()
            # Remove common stopwords
            stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
            return [t for t in tokens if t not in stopwords and len(t) > 2]
        
        def expand_synonyms(tokens):
            """Expand common tech synonyms"""
            synonym_map = {
                'ml': ['machine', 'learning', 'machinelearning'],
                'ai': ['artificial', 'intelligence', 'artificialintelligence'],
                'dl': ['deep', 'learning', 'deeplearning'],
                'nlp': ['natural', 'language', 'processing'],
                'cv': ['computer', 'vision'],
                'iot': ['internet', 'things', 'embedded'],
                'cloud': ['aws', 'azure', 'gcp', 'distributed'],
                'blockchain': ['crypto', 'distributed', 'ledger'],
                'data': ['analytics', 'science', 'mining'],
                'web': ['frontend', 'backend', 'fullstack'],
                'mobile': ['android', 'ios', 'app'],
                'security': ['cyber', 'cryptography', 'encryption'],
            }
            expanded = set(tokens)
            for token in tokens:
                if token in synonym_map:
                    expanded.update(synonym_map[token])
            return list(expanded)
        
        def calculate_tf_idf(documents):
            """Calculate TF-IDF vectors for documents"""
            # Build vocabulary
            vocab = set()
            for doc in documents:
                vocab.update(doc)
            vocab = list(vocab)
            
            # Calculate IDF
            idf = {}
            num_docs = len(documents)
            for word in vocab:
                doc_count = sum(1 for doc in documents if word in doc)
                idf[word] = math.log(num_docs / (1 + doc_count))
            
            # Calculate TF-IDF vectors
            vectors = []
            for doc in documents:
                word_freq = Counter(doc)
                vector = {}
                for word in vocab:
                    tf = word_freq.get(word, 0) / max(len(doc), 1)
                    vector[word] = tf * idf[word]
                vectors.append(vector)
            
            return vectors, vocab
        
        def cosine_similarity(vec1, vec2, vocab):
            """Calculate cosine similarity between two vectors"""
            dot_product = sum(vec1.get(word, 0) * vec2.get(word, 0) for word in vocab)
            mag1 = math.sqrt(sum(v**2 for v in vec1.values()))
            mag2 = math.sqrt(sum(v**2 for v in vec2.values()))
            
            if mag1 == 0 or mag2 == 0:
                return 0
            return dot_product / (mag1 * mag2)
        
        # 4. Prepare documents for TF-IDF
        faculty_docs = []
        theme_docs = []
        
        for faculty_id, interests, faculty_name in unassigned_faculty:
            tokens = normalize_text(interests)
            tokens = expand_synonyms(tokens)
            faculty_docs.append(tokens)
        
        for theme_id, theme_name, theme_desc, max_mentors, current_count in themes:
            theme_text = f"{theme_name} {theme_desc or ''}"
            tokens = normalize_text(theme_text)
            tokens = expand_synonyms(tokens)
            theme_docs.append(tokens)
        
        # 5. Calculate TF-IDF vectors
        all_docs = faculty_docs + theme_docs
        tfidf_vectors, vocab = calculate_tf_idf(all_docs)
        
        faculty_vectors = tfidf_vectors[:len(faculty_docs)]
        theme_vectors = tfidf_vectors[len(faculty_docs):]
        
        # 6. 🎯 Intelligent Matching with Constraints
        assignments = []
        assignment_log = []
        theme_counts = {t[0]: t[4] for t in themes}  # ThemeID -> CurrentCount
        theme_max = {t[0]: t[3] for t in themes}  # ThemeID -> MaxMentors
        
        for i, (faculty_id, interests, faculty_name) in enumerate(unassigned_faculty):
            best_match = None
            best_score = 0
            
            for j, (theme_id, theme_name, theme_desc, max_mentors, current_count) in enumerate(themes):
                # Skip if theme at capacity
                if theme_counts[theme_id] >= theme_max[theme_id]:
                    continue
                
                # 🧠 Calculate semantic similarity
                similarity = cosine_similarity(faculty_vectors[i], theme_vectors[j], vocab)
                
                # Scale to 0-100
                base_score = similarity * 100
                
                # Load balancing bonus (prefer less loaded themes)
                load_factor = (theme_max[theme_id] - theme_counts[theme_id]) / theme_max[theme_id]
                load_bonus = load_factor * 20
                
                final_score = base_score + load_bonus
                
                if final_score > best_score and final_score > 10:  # Minimum threshold
                    best_score = final_score
                    best_match = (theme_id, theme_name)
            
            # Assign if we found a match
            if best_match:
                theme_id, theme_name = best_match
                assignments.append((faculty_id, theme_id))
                assignment_log.append({
                    'faculty_id': faculty_id,
                    'faculty_name': faculty_name,
                    'theme_id': theme_id,
                    'theme_name': theme_name,
                    'score': round(best_score, 2),
                    'interests': interests,
                    'method': 'NLP-TF-IDF'
                })
                
                # Update count for load balancing
                theme_counts[theme_id] += 1
        
        # 7. Execute assignments in a transaction
        if assignments:
            for faculty_id, theme_id in assignments:
                cur.execute("""
                    INSERT INTO FacultyTheme (FacultyUserID, ThemeID)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE ThemeID = VALUES(ThemeID)
                """, (faculty_id, theme_id))
            
            mysql.connection.commit()
            
        return jsonify({
            'message': f'🤖 AI-powered assignment completed: {len(assignments)} faculty assigned',
            'assignments': assignment_log,
            'total_processed': len(unassigned_faculty),
            'algorithm': 'TF-IDF Semantic Similarity with Constraint Solving'
        }), 200
        
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()

# ✅ NEW: Analytics Endpoint
@admin_bp.route('/analytics', methods=['GET'])
@jwt_required()
@roles_required('Admin')
def get_analytics():
    """
    Comprehensive analytics for admin dashboard
    """
    cur = mysql.connection.cursor()
    try:
        analytics = {}
        
        # 1. Projects per Theme
        cur.execute("""
            SELECT t.ThemeName, COUNT(p.ProjectID) as project_count
            FROM Theme t
            LEFT JOIN Project p ON t.ThemeID = p.ThemeID
            GROUP BY t.ThemeID, t.ThemeName
            ORDER BY project_count DESC
        """)
        analytics['projects_by_theme'] = [
            {'theme': row[0], 'count': row[1]} for row in cur.fetchall()
        ]
        
        # 2. Avg Scores by Phase
        cur.execute("""
            SELECT Phase, AVG(Score) as avg_score, COUNT(*) as eval_count
            FROM evaluation
            GROUP BY Phase
            ORDER BY Phase
        """)
        analytics['avg_scores_by_phase'] = [
            {'phase': row[0], 'avg_score': round(float(row[1]), 2) if row[1] else 0, 'count': row[2]}
            for row in cur.fetchall()
        ]
        
        # 3. Faculty Workload (Mentor + Judge counts)
        cur.execute("""
            SELECT 
                u.UserID, 
                u.Name,
                COUNT(DISTINCT ma.ProjectID) as mentor_count,
                COUNT(DISTINCT ja.ProjectID) as judge_count
            FROM User u
            JOIN Faculty f ON u.UserID = f.UserID
            LEFT JOIN mentorassignment ma ON u.UserID = ma.FacultyUserID
            LEFT JOIN judgeassignment ja ON u.UserID = ja.FacultyUserID
            GROUP BY u.UserID, u.Name
            HAVING mentor_count > 0 OR judge_count > 0
            ORDER BY (mentor_count + judge_count) DESC
        """)
        analytics['faculty_workload'] = [
            {
                'faculty_id': row[0],
                'name': row[1],
                'mentor_count': row[2],
                'judge_count': row[3],
                'total': row[2] + row[3]
            }
            for row in cur.fetchall()
        ]
        
        # 4. Theme Assignment Coverage
        cur.execute("""
            SELECT t.ThemeName, COUNT(ft.FacultyUserID) as faculty_count
            FROM Theme t
            LEFT JOIN FacultyTheme ft ON t.ThemeID = ft.ThemeID
            GROUP BY t.ThemeID, t.ThemeName
            ORDER BY faculty_count DESC
        """)
        analytics['theme_coverage'] = [
            {'theme': row[0], 'faculty_count': row[1]} for row in cur.fetchall()
        ]
        
        # 5. Overall Stats
        cur.execute("SELECT COUNT(*) FROM Project")
        total_projects = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM User WHERE Role='Student'")
        total_students = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM User WHERE Role='Faculty'")
        total_faculty = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM Theme")
        total_themes = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(DISTINCT FacultyUserID) FROM FacultyTheme")
        assigned_faculty = cur.fetchone()[0]
        
        analytics['overall'] = {
            'total_projects': total_projects,
            'total_students': total_students,
            'total_faculty': total_faculty,
            'total_themes': total_themes,
            'assigned_faculty': assigned_faculty,
            'unassigned_faculty': total_faculty - assigned_faculty
        }
        
        return jsonify(analytics), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()

# ✅ NEW: Get unassigned faculty for dropdown
@admin_bp.route('/unassigned_faculty', methods=['GET'])
@jwt_required()
@roles_required('Admin')
def get_unassigned_faculty():
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            SELECT u.UserID, u.Name, f.Dept, f.Interests
            FROM User u
            JOIN Faculty f ON u.UserID = f.UserID
            LEFT JOIN FacultyTheme ft ON u.UserID = ft.FacultyUserID
            WHERE ft.FacultyUserID IS NULL
            ORDER BY u.Name
        """)
        rows = cur.fetchall()
        faculty = [
            {
                'UserID': row[0],
                'Name': row[1],
                'Dept': row[2],
                'Interests': row[3] or ''
            }
            for row in rows
        ]
        return jsonify({'faculty': faculty}), 200
    finally:
        cur.close()

# ✅ NEW: Detailed Theme Distribution
@admin_bp.route('/themes/distribution', methods=['GET'])
@jwt_required()
@roles_required('Admin')
def get_theme_distribution():
    """Get detailed distribution of faculty and projects per theme"""
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            SELECT 
                t.ThemeID,
                t.ThemeName,
                t.Description,
                COALESCE(t.MaxMentors, 5) as MaxMentors,
                COUNT(DISTINCT ft.FacultyUserID) as AssignedFaculty,
                COUNT(DISTINCT p.ProjectID) as TotalProjects,
                COUNT(DISTINCT CASE WHEN p.Status = 'Approved' THEN p.ProjectID END) as ApprovedProjects
            FROM Theme t
            LEFT JOIN FacultyTheme ft ON t.ThemeID = ft.ThemeID
            LEFT JOIN Project p ON t.ThemeID = p.ThemeID
            GROUP BY t.ThemeID, t.ThemeName, t.Description, t.MaxMentors
            ORDER BY TotalProjects DESC
        """)
        rows = cur.fetchall()
        distribution = [
            {
                'theme_id': row[0],
                'theme_name': row[1],
                'description': row[2],
                'max_mentors': row[3],
                'assigned_faculty': row[4],
                'capacity_used': f"{row[4]}/{row[3]}",
                'total_projects': row[5],
                'approved_projects': row[6],
                'capacity_percentage': round((row[4] / row[3]) * 100, 1) if row[3] > 0 else 0
            }
            for row in rows
        ]
        return jsonify({'distribution': distribution}), 200
    finally:
        cur.close()

# ✅ NEW: Student-Mentor Mapping
@admin_bp.route('/mappings/student-mentor', methods=['GET'])
@jwt_required()
@roles_required('Admin')
def get_student_mentor_mapping():
    """Get detailed mapping of which students are mentored by whom"""
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            SELECT 
                s.UserID as StudentID,
                u1.Name as StudentName,
                tm.ProjectID,
                p.Title as ProjectTitle,
                t.ThemeName,
                ma.FacultyUserID as MentorID,
                u2.Name as MentorName
            FROM Student s
            JOIN User u1 ON s.UserID = u1.UserID
            JOIN TeamMember tm ON s.UserID = tm.UserID
            JOIN Project p ON tm.ProjectID = p.ProjectID
            JOIN Theme t ON p.ThemeID = t.ThemeID
            LEFT JOIN mentorassignment ma ON p.ProjectID = ma.ProjectID
            LEFT JOIN User u2 ON ma.FacultyUserID = u2.UserID
            ORDER BY t.ThemeName, p.Title, s.UserID
        """)
        rows = cur.fetchall()
        mappings = [
            {
                'student_id': row[0],
                'student_name': row[1],
                'project_id': row[2],
                'project_title': row[3],
                'theme': row[4],
                'mentor_id': row[5],
                'mentor_name': row[6] or 'Unassigned'
            }
            for row in rows
        ]
        return jsonify({'mappings': mappings, 'total': len(mappings)}), 200
    finally:
        cur.close()

# ✅ NEW: Project-Judge Mapping
@admin_bp.route('/mappings/project-judge', methods=['GET'])
@jwt_required()
@roles_required('Admin')
def get_project_judge_mapping():
    """Get detailed mapping of which judges are assigned to which projects"""
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            SELECT 
                p.ProjectID,
                p.Title as ProjectTitle,
                t.ThemeName,
                p.Status,
                ja.FacultyUserID as JudgeID,
                u.Name as JudgeName,
                ja.SelectionType,
                COUNT(DISTINCT tm.UserID) as TeamSize
            FROM Project p
            JOIN Theme t ON p.ThemeID = t.ThemeID
            LEFT JOIN judgeassignment ja ON p.ProjectID = ja.ProjectID
            LEFT JOIN User u ON ja.FacultyUserID = u.UserID
            LEFT JOIN TeamMember tm ON p.ProjectID = tm.ProjectID
            GROUP BY p.ProjectID, p.Title, t.ThemeName, p.Status, ja.FacultyUserID, u.Name, ja.SelectionType
            ORDER BY t.ThemeName, p.ProjectID
        """)
        rows = cur.fetchall()
        mappings = [
            {
                'project_id': row[0],
                'project_title': row[1],
                'theme': row[2],
                'status': row[3],
                'judge_id': row[4],
                'judge_name': row[5] or 'Unassigned',
                'selection_type': row[6] or 'N/A',
                'team_size': row[7]
            }
            for row in rows
        ]
        return jsonify({'mappings': mappings, 'total': len(mappings)}), 200
    finally:
        cur.close()

# ✅ NEW: Detailed Project Info with All Relationships
@admin_bp.route('/projects/detailed', methods=['GET'])
@jwt_required()
@roles_required('Admin')
def get_detailed_projects():
    """Get comprehensive project details with all relationships"""
    theme_filter = request.args.get('theme')
    status_filter = request.args.get('status')
    
    cur = mysql.connection.cursor()
    try:
        query = """
            SELECT 
                p.ProjectID,
                p.Title,
                p.Abstract,
                p.Status,
                t.ThemeID,
                t.ThemeName,
                COUNT(DISTINCT tm.UserID) as TeamSize,
                GROUP_CONCAT(DISTINCT u1.Name SEPARATOR ', ') as TeamMembers,
                GROUP_CONCAT(DISTINCT CONCAT(u2.Name, ' (Mentor)') SEPARATOR ', ') as Mentors,
                GROUP_CONCAT(DISTINCT CONCAT(u3.Name, ' (Judge)') SEPARATOR ', ') as Judges
            FROM Project p
            JOIN Theme t ON p.ThemeID = t.ThemeID
            LEFT JOIN TeamMember tm ON p.ProjectID = tm.ProjectID
            LEFT JOIN User u1 ON tm.UserID = u1.UserID
            LEFT JOIN mentorassignment ma ON p.ProjectID = ma.ProjectID
            LEFT JOIN User u2 ON ma.FacultyUserID = u2.UserID
            LEFT JOIN judgeassignment ja ON p.ProjectID = ja.ProjectID
            LEFT JOIN User u3 ON ja.FacultyUserID = u3.UserID
        """
        
        filters = []
        params = []
        
        if theme_filter:
            filters.append("t.ThemeID = %s")
            params.append(theme_filter)
        
        if status_filter:
            filters.append("p.Status = %s")
            params.append(status_filter)
        
        if filters:
            query += " WHERE " + " AND ".join(filters)
        
        query += """
            GROUP BY p.ProjectID, p.Title, p.Abstract, p.Status, t.ThemeID, t.ThemeName
            ORDER BY t.ThemeName, p.ProjectID
        """
        
        cur.execute(query, params)
        rows = cur.fetchall()
        
        projects = [
            {
                'project_id': row[0],
                'title': row[1],
                'abstract': row[2],
                'status': row[3],
                'theme_id': row[4],
                'theme_name': row[5],
                'team_size': row[6],
                'team_members': row[7] or 'No team members',
                'mentors': row[8] or 'No mentors assigned',
                'judges': row[9] or 'No judges assigned'
            }
            for row in rows
        ]
        
        return jsonify({'projects': projects, 'total': len(projects)}), 200
    finally:
        cur.close()

# ✅ NEW: Faculty Details with All Assignments
@admin_bp.route('/faculty/detailed', methods=['GET'])
@jwt_required()
@roles_required('Admin')
def get_detailed_faculty():
    """Get comprehensive faculty details with all assignments"""
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            SELECT 
                u.UserID,
                u.Name,
                u.Email,
                f.Dept,
                f.Interests,
                t.ThemeID,
                t.ThemeName,
                COUNT(DISTINCT ma.ProjectID) as MentorCount,
                COUNT(DISTINCT ja.ProjectID) as JudgeCount,
                GROUP_CONCAT(DISTINCT p1.Title SEPARATOR ' | ') as MentorProjects,
                GROUP_CONCAT(DISTINCT p2.Title SEPARATOR ' | ') as JudgeProjects
            FROM User u
            JOIN Faculty f ON u.UserID = f.UserID
            LEFT JOIN FacultyTheme ft ON u.UserID = ft.FacultyUserID
            LEFT JOIN Theme t ON ft.ThemeID = t.ThemeID
            LEFT JOIN mentorassignment ma ON u.UserID = ma.FacultyUserID
            LEFT JOIN Project p1 ON ma.ProjectID = p1.ProjectID
            LEFT JOIN judgeassignment ja ON u.UserID = ja.FacultyUserID
            LEFT JOIN Project p2 ON ja.ProjectID = p2.ProjectID
            GROUP BY u.UserID, u.Name, u.Email, f.Dept, f.Interests, t.ThemeID, t.ThemeName
            ORDER BY u.Name
        """)
        rows = cur.fetchall()
        
        faculty = [
            {
                'faculty_id': row[0],
                'name': row[1],
                'email': row[2],
                'department': row[3],
                'interests': row[4] or 'Not specified',
                'theme_id': row[5],
                'theme_name': row[6] or 'Unassigned',
                'mentor_count': row[7],
                'judge_count': row[8],
                'total_load': row[7] + row[8],
                'mentor_projects': row[9] or 'None',
                'judge_projects': row[10] or 'None'
            }
            for row in rows
        ]
        
        return jsonify({'faculty': faculty, 'total': len(faculty)}), 200
    finally:
        cur.close()

# ✅ NEW: Plagiarism Detection for Submissions
@admin_bp.route('/plagiarism/check', methods=['POST'])
@jwt_required()
@roles_required('Admin')
def check_plagiarism():
    """
    Check plagiarism for submissions using cosine similarity
    Supports both text content and URL fetching
    """
    import re
    from collections import Counter
    import math
    import requests
    from bs4 import BeautifulSoup
    
    data = request.json
    submission_id = data.get('submission_id')
    
    if not submission_id:
        return jsonify({'error': 'Submission ID required'}), 400
    
    cur = mysql.connection.cursor()
    try:
        # Get target submission
        cur.execute("""
            SELECT s.SubmissionID, s.SubmissionContent, p.Title, p.ProjectID
            FROM submission s
            JOIN Project p ON s.ProjectID = p.ProjectID
            WHERE s.SubmissionID = %s
        """, (submission_id,))
        target = cur.fetchone()
        
        if not target or not target[1]:
            return jsonify({'error': 'Submission not found or no content'}), 404
        
        sub_id, content, project_title, project_id = target
        
        # Extract text content
        def extract_text_from_url(url):
            """Fetch and extract text from URL"""
            try:
                # Check if it's a Google Drive link
                if 'drive.google.com' in url:
                    # Extract file ID and convert to direct download
                    if '/file/d/' in url:
                        file_id = url.split('/file/d/')[1].split('/')[0]
                        url = f'https://drive.google.com/uc?export=download&id={file_id}'
                
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers, timeout=10)
                
                # Try to extract text from HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                return text[:10000]  # Limit to first 10k chars
                
            except Exception as e:
                return f"[URL content: {url}]"  # Fallback to URL as text
        
        # Process content - check if it's a URL
        target_text = content
        if content.startswith('http://') or content.startswith('https://'):
            target_text = extract_text_from_url(content)
        
        # Get all other submissions for comparison
        cur.execute("""
            SELECT s.SubmissionID, s.SubmissionContent, p.Title, p.ProjectID
            FROM submission s
            JOIN Project p ON s.ProjectID = p.ProjectID
            WHERE s.SubmissionID != %s AND s.SubmissionContent IS NOT NULL AND s.SubmissionContent != ''
        """, (submission_id,))
        all_submissions = cur.fetchall()
        
        if not all_submissions:
            return jsonify({
                'submission_id': submission_id,
                'project_title': project_title,
                'plagiarism_score': 0,
                'status': 'SAFE',
                'matches': [],
                'message': 'No other submissions to compare against'
            }), 200
        
        # Text processing functions
        def normalize_text(text):
            if not text:
                return []
            text = text.lower()
            text = re.sub(r'[^a-z0-9\s]', '', text)
            words = text.split()
            stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'http', 'https', 'www', 'com'}
            return [w for w in words if w not in stopwords and len(w) > 2]
        
        def calculate_similarity(text1, text2):
            words1 = normalize_text(text1)
            words2 = normalize_text(text2)
            
            if not words1 or not words2:
                return 0
            
            # Count word frequencies
            freq1 = Counter(words1)
            freq2 = Counter(words2)
            
            # Get all unique words
            all_words = set(freq1.keys()) | set(freq2.keys())
            
            # Calculate cosine similarity
            dot_product = sum(freq1.get(word, 0) * freq2.get(word, 0) for word in all_words)
            mag1 = math.sqrt(sum(v**2 for v in freq1.values()))
            mag2 = math.sqrt(sum(v**2 for v in freq2.values()))
            
            if mag1 == 0 or mag2 == 0:
                return 0
            
            return (dot_product / (mag1 * mag2)) * 100
        
        # Check against all submissions
        matches = []
        max_similarity = 0
        
        for other_id, other_content, other_title, other_project_id in all_submissions:
            # Extract text from URL if needed
            other_text = other_content
            if other_content.startswith('http://') or other_content.startswith('https://'):
                other_text = extract_text_from_url(other_content)
            
            similarity = calculate_similarity(target_text, other_text)
            
            if similarity > 15:  # Lower threshold for submissions
                matches.append({
                    'submission_id': other_id,
                    'project_title': other_title,
                    'project_id': other_project_id,
                    'similarity_score': round(similarity, 2),
                    'status': 'HIGH' if similarity > 60 else 'MEDIUM' if similarity > 30 else 'LOW',
                    'content_preview': other_content[:100] + '...' if len(other_content) > 100 else other_content
                })
                max_similarity = max(max_similarity, similarity)
        
        # Sort by similarity
        matches.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        # Determine overall status
        if max_similarity > 60:
            status = 'FAILED'
            color = 'error'
        elif max_similarity > 30:
            status = 'WARNING'
            color = 'warning'
        else:
            status = 'SAFE'
            color = 'success'
        
        return jsonify({
            'submission_id': submission_id,
            'project_title': project_title,
            'submission_content': content[:200] + '...' if len(content) > 200 else content,
            'plagiarism_score': round(max_similarity, 2),
            'status': status,
            'color': color,
            'matches': matches[:10],  # Top 10 matches
            'total_matches': len(matches),
            'message': f'Found {len(matches)} potential matches',
            'is_url': content.startswith('http://') or content.startswith('https://')
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()

# ✅ NEW: Get All Submissions for Plagiarism Check
@admin_bp.route('/submissions/all', methods=['GET'])
@jwt_required()
@roles_required('Admin')
def get_all_submissions():
    """Get all submissions with project details for plagiarism checking"""
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            SELECT 
                s.SubmissionID,
                s.SubmissionContent,
                s.SubmittedAt,
                p.ProjectID,
                p.Title as ProjectTitle,
                t.ThemeName
            FROM submission s
            JOIN Project p ON s.ProjectID = p.ProjectID
            JOIN Theme t ON p.ThemeID = t.ThemeID
            WHERE s.SubmissionContent IS NOT NULL AND s.SubmissionContent != ''
            ORDER BY s.SubmittedAt DESC
        """)
        rows = cur.fetchall()
        
        submissions = [
            {
                'submission_id': row[0],
                'content': row[1][:100] + '...' if len(row[1]) > 100 else row[1],
                'full_content': row[1],
                'submitted_at': row[2].strftime('%Y-%m-%d %H:%M') if row[2] else 'N/A',
                'project_id': row[3],
                'project_title': row[4],
                'theme': row[5],
                'is_url': row[1].startswith('http://') or row[1].startswith('https://') if row[1] else False
            }
            for row in rows
        ]
        
        return jsonify({'submissions': submissions, 'total': len(submissions)}), 200
    finally:
        cur.close()

# ✅ NEW: Insights & Recommendations (Quick Win Feature)
@admin_bp.route('/insights', methods=['GET'])
@jwt_required()
@roles_required('Admin')
def get_insights():
    """
    Quick Win: Insights and Recommendations Dashboard
    """
    cur = mysql.connection.cursor()
    try:
        insights = {}
        
        # 1. Project Health Scores
        cur.execute("""
            SELECT 
                p.ProjectID,
                p.Title,
                t.ThemeName,
                p.Status,
                COUNT(DISTINCT s.SubmissionID) as SubmissionCount,
                COUNT(DISTINCT e.EvaluationID) as EvaluationCount,
                COUNT(DISTINCT tm.UserID) as TeamSize,
                AVG(e.Score) as AvgScore
            FROM Project p
            JOIN Theme t ON p.ThemeID = t.ThemeID
            LEFT JOIN submission s ON p.ProjectID = s.ProjectID
            LEFT JOIN evaluation e ON p.ProjectID = e.ProjectID
            LEFT JOIN TeamMember tm ON p.ProjectID = tm.ProjectID
            GROUP BY p.ProjectID, p.Title, t.ThemeName, p.Status
        """)
        projects = cur.fetchall()
        
        project_health = []
        for row in projects:
            # Calculate health score (0-100)
            health_score = 0
            health_score += min((row[4] / 3) * 30, 30)  # Submissions (max 30 points)
            health_score += min((row[5] / 10) * 30, 30)  # Evaluations (max 30 points)
            health_score += min((row[7] or 0) * 4, 40)  # Avg score (max 40 points)
            
            status = 'HEALTHY' if health_score > 70 else 'AT_RISK' if health_score > 40 else 'CRITICAL'
            color = 'success' if health_score > 70 else 'warning' if health_score > 40 else 'error'
            
            project_health.append({
                'project_id': row[0],
                'title': row[1],
                'theme': row[2],
                'status': row[3],
                'health_score': round(health_score, 1),
                'health_status': status,
                'color': color,
                'submissions': row[4],
                'evaluations': row[5],
                'team_size': row[6],
                'avg_score': round(float(row[7]), 2) if row[7] else 0
            })
        
        # Sort by health score
        project_health.sort(key=lambda x: x['health_score'])
        insights['project_health'] = project_health
        
        # 2. Top Performers (Students)
        cur.execute("""
            SELECT 
                s.UserID,
                u.Name,
                AVG(e.Score) as AvgScore,
                COUNT(DISTINCT e.EvaluationID) as TotalEvaluations
            FROM Student s
            JOIN User u ON s.UserID = u.UserID
            LEFT JOIN evaluation e ON s.UserID = e.StudentUserID
            GROUP BY s.UserID, u.Name
            HAVING TotalEvaluations > 0
            ORDER BY AvgScore DESC
            LIMIT 10
        """)
        top_students = [
            {
                'student_id': row[0],
                'name': row[1],
                'avg_score': round(float(row[2]), 2),
                'total_evaluations': row[3]
            }
            for row in cur.fetchall()
        ]
        insights['top_performers'] = top_students
        
        # 3. At-Risk Projects (low submission rate)
        at_risk = [p for p in project_health if p['health_status'] in ['AT_RISK', 'CRITICAL']]
        insights['at_risk_projects'] = at_risk[:10]
        
        # 4. Theme Popularity
        cur.execute("""
            SELECT 
                t.ThemeName,
                COUNT(p.ProjectID) as ProjectCount,
                AVG(
                    (SELECT AVG(e.Score) 
                     FROM evaluation e 
                     JOIN TeamMember tm ON e.StudentUserID = tm.UserID
                     WHERE tm.ProjectID = p.ProjectID)
                ) as ThemeAvgScore
            FROM Theme t
            LEFT JOIN Project p ON t.ThemeID = p.ThemeID
            GROUP BY t.ThemeID, t.ThemeName
            ORDER BY ProjectCount DESC
        """)
        theme_popularity = [
            {
                'theme': row[0],
                'project_count': row[1],
                'avg_score': round(float(row[2]), 2) if row[2] else 0,
                'popularity': 'HIGH' if row[1] > 5 else 'MEDIUM' if row[1] > 2 else 'LOW'
            }
            for row in cur.fetchall()
        ]
        insights['theme_popularity'] = theme_popularity
        
        # 5. Faculty Performance
        cur.execute("""
            SELECT 
                u.UserID,
                u.Name,
                COUNT(DISTINCT ma.ProjectID) as MentorCount,
                AVG(
                    (SELECT AVG(e.Score)
                     FROM evaluation e
                     JOIN TeamMember tm ON e.StudentUserID = tm.UserID
                     WHERE tm.ProjectID = ma.ProjectID)
                ) as AvgMentorScore
            FROM User u
            JOIN Faculty f ON u.UserID = f.UserID
            LEFT JOIN mentorassignment ma ON u.UserID = ma.FacultyUserID
            GROUP BY u.UserID, u.Name
            HAVING MentorCount > 0
            ORDER BY AvgMentorScore DESC
            LIMIT 10
        """)
        faculty_performance = [
            {
                'faculty_id': row[0],
                'name': row[1],
                'mentor_count': row[2],
                'avg_mentee_score': round(float(row[3]), 2) if row[3] else 0
            }
            for row in cur.fetchall()
        ]
        insights['faculty_performance'] = faculty_performance
        
        # 6. Completion Rate
        cur.execute("""
            SELECT 
                COUNT(*) as TotalProjects,
                SUM(CASE WHEN Status = 'Approved' THEN 1 ELSE 0 END) as ApprovedProjects,
                SUM(CASE WHEN Status = 'Rejected' THEN 1 ELSE 0 END) as RejectedProjects,
                SUM(CASE WHEN Status = 'Pending' THEN 1 ELSE 0 END) as PendingProjects
            FROM Project
        """)
        row = cur.fetchone()
        total = row[0]
        insights['completion_rate'] = {
            'total_projects': total,
            'approved': row[1],
            'rejected': row[2],
            'pending': row[3],
            'approval_rate': round((row[1] / total) * 100, 1) if total > 0 else 0,
            'completion_percentage': round(((row[1] + row[2]) / total) * 100, 1) if total > 0 else 0
        }
        
        return jsonify(insights), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()

