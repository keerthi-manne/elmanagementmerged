# EXPERIENTIAL LEARNING MANAGEMENT SYSTEM

**Report**

**Database Management Systems**

**Submitted By**
[Student Name 1] ([USN 1])
[Student Name 2] ([USN 2])

**Under the Guidance of**
[Guide Name]
[Designation]

**RV COLLEGE OF ENGINEERING ®**
(Autonomous Institution Affiliated to VTU, Belagavi)
Bengaluru-560059

**Department of Information Science and Engineering**
**2025-26**

---

## CERTIFICATE

Certified that the project work titled **"Experiential Learning Management System"** is carried out by **[Student Name 1]** and **[Student Name 2]** who are bonafide students of RV College of Engineering, Bengaluru, in partial fulfillment for the award of degree of **Bachelor of Engineering** in **Information Science and Engineering** of the Visvesvaraya Technological University, Belagavi during the academic year 2025-26. It is certified that all corrections/suggestions indicated for the Internal Assessment have been incorporated in the report deposited in the departmental library. The report has been approved as it satisfies the academic requirements in respect of experiential learning work prescribed by the institution for the said degree.

**[Guide Name]**
[Designation]
Department of ISE, RVCE

**Dr. [HOD Name]**
Head of the Department
Department of ISE, RVCE

---

## DECLARATION

We, **[Student Name 1]** and **[Student Name 2]**, students of 5th semester B.E., Department of Information Science and Engineering, RV College of Engineering, Bengaluru, hereby declare that the Experiential Learning (EL) project titled **"Experiential Learning Management System"** has been carried out by us and submitted in partial fulfillment for the award of degree of **Bachelor of Engineering** in **Information Science and Engineering** during the academic year 2025-26.

We also declare that any Intellectual Property Rights generated out of this project carried out at RVCE will be the property of RV College of Engineering, Bengaluru and we will be one of the authors of the same.

Place: Bengaluru
Date: [Current Date]

[Signature 1]
**[Student Name 1]**

[Signature 2]
**[Student Name 2]**

---

## CONTENTS

1.  **Introduction**
    *   1.1 Terminology
    *   1.2 Purpose
    *   1.3 Motivation
    *   1.4 Problem Statement
    *   1.5 Objectives
    *   1.6 Scope and Relevance
2.  **Requirement Specification**
    *   2.1 Functional Requirements
    *   2.2 Non-Functional Requirements
    *   2.3 Hardware & Software Requirements
3.  **Design**
    *   3.1 E-R Diagram
    *   3.2 Data Flow Diagram
    *   3.3 Relational Schema and Normalization
    *   3.4 Front End Design
4.  **Implementation Details**
    *   4.1 Database Implementation
    *   4.2 Backend Implementation
    *   4.3 Front End Implementation
5.  **Testing and Results**
    *   5.1 Database Testing
    *   5.2 System Testing
6.  **Conclusion**
    *   6.1 Future Enhancements
    *   6.2 Bibliography

---

# 1. INTRODUCTION

## 1.1 Terminology

| Term | Definition |
| :--- | :--- |
| **EL** | Experiential Learning – a project-based learning initiative. |
| **RBAC** | Role-Based Access Control – regulating access based on user roles (Admin, Faculty, Student). |
| **DBMS** | Database Management System. |
| **API** | Application Programming Interface – allows communication between frontend and backend. |
| **SPA** | Single Page Application – web app implementation for fluid user experience. |
| **Jupyter/AI** | usage of AI models for plagiarism detection and analytics. |
| **USN** | University Serial Number - unique identifier for students. |

## 1.2 Purpose

The **Experiential Learning Management System (ELMS)** is a comprehensive web-based platform designed to streamline the management of Experiential Learning projects at RV College of Engineering. It facilitates the entire lifecycle of an EL project, from team formation and topic selection to report submission and evaluation. The system acts as a central repository for project data, enabling seamless collaboration between students, mentors, and administrators.

## 1.3 Motivation

Currently, the management of EL projects involves disjointed tools such as spreadsheets, manual emails, and isolated file submissions. This manual approach leads to:
*   Difficulty in tracking team formations and ensuring diversity.
*   Redundant data entry and inconsistency.
*   Challenges in monitoring project progress and submission deadlines.
*   Lack of centralized analytics on student performance and project domains.
*   Manual effort in plagiarism checking and ensuring project uniqueness.

A dedicated DBMS-backed application is required to automate these processes, ensure data integrity, and provide real-time insights.

## 1.4 Problem Statement

The Department requires a unified system to manage hundreds of student projects simultaneously. The existing manual system fails to provide:
*   Real-time validation of team constraints (e.g., team size, inter-disciplinary mix).
*   Automated mapping of mentors and judges to teams.
*   A secure and organized way to handle phase-wise submissions (Proposal, Phase 1, Phase 2).
*   Integrated plagiarism checks to ensure academic integrity.

The EL Management System aims to resolve these issues by digitizing the entire workflow.

## 1.5 Objectives

*   **Centralized Data Management**: To store and manage data regarding students, faculties, courses, teams, and projects in a relational database.
*   **Process Automation**: To automate team formation validation, mentor allocation, and deadline enforcement.
*   **Evaluation & Grading**: To provide a digital interface for faculty to grade submissions and provide feedback.
*   **Analytics**: To provide dashboards showing project domain distribution, average scores, and pending submissions.
*   **Integrity**: To implement logic preventing duplicate topics and enabling plagiarism detection.

## 1.6 Scope and Relevance

**Scope**: The system is designed for the ISE department but is scalable to other departments. It covers three main roles:
1.  **Admin**: System configuration, user management, and overall monitoring.
2.  **Faculty**: Mentoring assigned teams, evaluating submissions as judges.
3.  **Student**: Profile management, team formation, project submission, and result viewing.

**Relevance**: This project directly impacts the efficiency of the academic curriculum delivery, reducing administrative burden and enhancing the student learning experience.

---

# 2. REQUIREMENT SPECIFICATION

## 2.1 Functional Requirements

### Administrator Module
*   The system shall allow admins to upload student and faculty data in bulk.
*   The system shall allow admins to define course details and project timelines.
*   The system shall provide an analytics dashboard for overall project status.
*   The system shall allow admins to allocate judges to project teams.

### Faculty Module (Mentor/Judge)
*   The system shall allow faculty to view teams assigned to them for mentoring.
*   The system shall allow faculty to view submissions (documents/links) for their assigned teams.
*   The system shall provide a grading interface to enter marks and comments for different project phases.
*   The system shall notify faculty of pending evaluations.

### Student Module
*   The system shall allow students to register and manage their profiles.
*   The system shall allow students to form teams by inviting peers using USNs.
*   The system shall validate team size and formation rules before finalizing.
*   The system shall allow teams to submit project details (Title, Abstract) and files for different phases.
*   The system shall allow students to view their grades and feedback.

### AI & Analytics Module
*   The system shall perform plagiarism checks on project abstracts/titles using cosine similarity or similar NLP techniques.
*   The system shall generate insights on the most popular domains/technologies used by students.

## 2.2 Non-Functional Requirements

*   **Security**: Passwords must be hashed. Access to specific routes must be restricted by role (RBAC).
*   **Performance**: The system should support concurrent access by 500+ students during submission deadlines.
*   **Scalability**: The database design should handle increasing data volume over academic years.
*   **Usability**: The UI should be responsive and intuitive, accessible on both desktop and mobile.
*   **Data Integrity**: Foreign key constraints must ensure no orphaned records (e.g., a team cannot exist without a valid project or members).

## 2.3 Hardware & Software Requirements

### Hardware
*   **Server**: Cloud-based or Local Server with 4GB+ RAM.
*   **Client**: Desktop/Laptop/Mobile with modern web browser.

### Software
*   **Operating System**: Windows / Linux / MacOS.
*   **Frontend**: React.js, Tailwind CSS, Vite.
*   **Backend**: Python, Flask, Flask-SQLAlchemy.
*   **Database**: SQLite (Development) / PostgreSQL (Production).
*   **Tools**: VS Code, Git, Postman.

---

# 3. DESIGN

## 3.1 E-R Diagram

*(Note: Insert the Entity-Relationship Diagram here. It should depict the entities User, Student, Faculty, Course, Project, Team, TeamMember, Submission, Evaluation and their relationships.)*

### 3.1.1 Entities and Attributes

1.  **USER**: `user_id` (PK), `email`, `password_hash`, `role`, `contact_number`.
2.  **STUDENT**: `student_id` (PK), `user_id` (FK), `srn`, `semester`, `section`, `cgpa`, `dept_id`.
3.  **FACULTY**: `faculty_id` (PK), `user_id` (FK), `dept_id`, `designation`.
4.  **COURSE**: `course_code` (PK), `name`, `credits`, `description`.
5.  **PROJECT**: `project_id` (PK), `title`, `description`, `domain`, `type`.
6.  **TEAM**: `team_id` (PK), `project_id` (FK), `mentor_id` (FK), `guide_id` (FK).
7.  **SUBMISSION**: `submission_id` (PK), `team_id` (FK), `phase` (Proposal/Phase1), `file_url`, `timestamp`.
8.  **EVALUATION**: `evaluation_id` (PK), `submission_id` (FK), `judge_id` (FK), `marks`, `comments`.

### 3.1.2 Relationships
*   **User to Student/Faculty**: One-to-One (Generalization).
*   **Faculty to Team (Mentor)**: One-to-Many.
*   **Team to Student**: One-to-Many (via TeamMember junction table).
*   **Team to Project**: One-to-One.
*   **Team to Submission**: One-to-Many (Multiple phases).
*   **Submission to Evaluation**: One-to-Many (Multiple judges may evaluate).

## 3.2 Relational Schema and Normalization

The database schema is designed to be in **Third Normal Form (3NF)** to ensure data consistency and minimize redundancy.

*   **1NF**: All attributes are atomic. No repeating groups (e.g., Team Members are stored in a separate `TeamMember` table, not as a comma-separated list in `Team`).
*   **2NF**: All non-key attributes are fully dependent on the primary key.
*   **3NF**: No transitive dependencies. (e.g., Department details are moved to a `Department` table if needed, though mostly handled via enum/code in this scope).

### Schema Structure
*(See Implementation Details for SQL definitions)*

## 3.4 Front End Design

The frontend is built using **React.js** with **Tailwind CSS** for a modern, responsive interface.
*   **Design Principles**: Component-based architecture, Clean UI, Response Feedback (Toasts).
*   **Navigation**:
    *   **Sidebar**: Dashboard, Teams, Projects, Evaluation (Context-sensitive based on Role).
    *   **Top Bar**: User Profile, Notifications, Logout.

---

# 4. IMPLEMENTATION DETAILS

## 4.1 Database Implementation

The system uses **SQLAlchemy ORM** to define models, which translates to SQL tables.

**Sample Model Definition (Python/SQLAlchemy):**

```python
class User(db.Model):
    user_id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'admin', 'student', 'faculty'

class Team(db.Model):
    team_id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    project_id = db.Column(db.String(36), db.ForeignKey('project.project_id'))
    mentor_id = db.Column(db.String(36), db.ForeignKey('faculty.faculty_id'))
```

**Security Features**:
*   **Password Hashing**: Uses `werkzeug.security.generate_password_hash` to store secure hashes.
*   **UUIDs**: Uses UUIDs for primary keys to prevent enumeration attacks.

## 4.2 Backend Implementation

The backend is a **RESTful API** developed with **Flask**.

**Key API Endpoints**:
*   `POST /api/auth/login`: Authenticates user and returns JWT/Session.
*   `POST /api/teams/create`: Validates rules and creates a new team.
*   `POST /api/submissions`: Handles file upload and record creation.
*   `GET /api/plagiarism/check`: Triggers the AI model to check content similarity.

## 4.3 Front End Implementation

The frontend consumes the REST API using **Axios**. State management ensures the UI reflects real-time data.

**Key Components**:
*   `StatsWidget.js`: Displays KPIs like "Total Teams", "Pending Evaluations".
*   `TeamForm.js`: Dynamic form for adding members.
*   `SubmissionHistory.js`: Timeline view of project submissions.

---

# 5. TESTING AND RESULTS

## 5.1 Database Testing

| Test Case ID | Description | Expected Result | Status |
| :--- | :--- | :--- | :--- |
| **DB-01** | Insert user with duplicate email | Error: Unique constraint violation | **PASS** |
| **DB-02** | Create team without Creator | Error: Non-null constraint violation | **PASS** |
| **DB-03** | Delete Project with existing Team | Error: Foreign Key violation (Integrity Error) | **PASS** |
| **DB-04** | Retrieve Students by Sem | Returns list of students for specific semester | **PASS** |

## 5.2 System Testing

| Test Case ID | Module | Actions | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **SYS-01** | Auth | Login with invalid password | "Invalid Credentials" message | **PASS** |
| **SYS-02** | Student | Invite student already in a team | Error: "Student already assigned" | **PASS** |
| **SYS-03** | Admin | Allocate Judge to Team | Judge can see Team in Dashboard | **PASS** |
| **SYS-04** | Faculty | Grade Submission | Marks updated in database | **PASS** |

---

# 6. CONCLUSION

The **Experiential Learning Management System** has been successfully designed and developed to address the challenges of manual project management. By leveraging modern web technologies and a robust database design, the system ensures:
*   Streamlined workflow for students and faculty.
*   Data integrity and security.
*   Fairness in evaluation through organized records.
*   Valuable insights through analytics.

## 6.1 Future Enhancements

*   **Integration with LMS**: Linking with Moodle/Canvas for grade syncing.
*   **Mobile App**: Native mobile application for push notifications.
*   **Advanced AI**: Automated grading assistance based on rubric matching.

## 6.2 Bibliography

1.  Flask Documentation: https://flask.palletsprojects.com/
2.  React Documentation: https://react.dev/
3.  "Database System Concepts", Silberschatz, Korth, Sudarshan.
4.  RVCE Academic Guidelines for Experiential Learning 2025.

---

**APPENDIX A: SCREENSHOTS**
*(Include screenshots of Login Page, Dashboards, and Forms here)*
