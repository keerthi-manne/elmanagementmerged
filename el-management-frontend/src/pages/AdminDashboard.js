import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import {
  approveProject,
  rejectProject,
  exportProjectsCSV,
} from '../api/faculty';
import StatsWidget from '../components/common/StatsWidget';
import PowerBIChart from '../components/common/PowerBIChart';
import SearchBar from '../components/common/SearchBar';
import axios from 'axios';

const API_BASE = 'http://localhost:5000';

function AdminDashboard() {
  const { authToken, userRole } = useAuth();

  // State
  const [activeTab, setActiveTab] = useState('analytics');
  const [analytics, setAnalytics] = useState(null);
  const [detailedProjects, setDetailedProjects] = useState([]);
  const [themeDistribution, setThemeDistribution] = useState([]);
  const [studentMentorMapping, setStudentMentorMapping] = useState([]);
  const [projectJudgeMapping, setProjectJudgeMapping] = useState([]);
  const [detailedFaculty, setDetailedFaculty] = useState([]);
  const [message, setMessage] = useState('');
  const [autoAssignLoading, setAutoAssignLoading] = useState(false);

  // Search states
  const [searchStudent, setSearchStudent] = useState('');
  const [searchProject, setSearchProject] = useState('');
  const [searchFaculty, setSearchFaculty] = useState('');
  const [searchTheme, setSearchTheme] = useState('');

  // Insights & Plagiarism
  const [insights, setInsights] = useState(null);
  const [plagiarismResult, setPlagiarismResult] = useState(null);
  const [checkingPlagiarism, setCheckingPlagiarism] = useState(false);
  const [selectedProjectForPlag, setSelectedProjectForPlag] = useState('');
  const [submissions, setSubmissions] = useState([]);

  // Filters
  const [themeFilter, setThemeFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  // Assignment state
  const [themes, setThemes] = useState([]);
  const [faculties, setFaculties] = useState([]);
  const [assignments, setAssignments] = useState([]);
  const [selectedFacultyId, setSelectedFacultyId] = useState('');
  const [selectedThemeId, setSelectedThemeId] = useState('');

  // New Management Form states
  const [userForm, setUserForm] = useState({
    user_id: '',
    name: '',
    email: '',
    password: '',
    role: 'Student',
    dept: '',
    semester: ''
  });
  const [themeForm, setThemeForm] = useState({
    ThemeName: '',
    Description: '',
    MaxMentors: 5
  });
  const [creatingUser, setCreatingUser] = useState(false);
  const [creatingTheme, setCreatingTheme] = useState(false);

  const loadAnalytics = useCallback(async () => {
    if (!authToken) return;
    try {
      const { data } = await axios.get(`${API_BASE}/admin/analytics`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      setAnalytics(data);
    } catch (err) {
      console.error('Analytics load error', err);
    }
  }, [authToken]);

  const loadThemeDistribution = useCallback(async () => {
    if (!authToken) return;
    try {
      const { data } = await axios.get(`${API_BASE}/admin/themes/distribution`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      setThemeDistribution(data.distribution || []);
    } catch (err) {
      console.error('Theme distribution load error', err);
    }
  }, [authToken]);

  const loadStudentMentorMapping = useCallback(async () => {
    if (!authToken) return;
    try {
      const { data } = await axios.get(`${API_BASE}/admin/mappings/student-mentor`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      setStudentMentorMapping(data.mappings || []);
    } catch (err) {
      console.error('Student-mentor mapping load error', err);
    }
  }, [authToken]);

  const loadProjectJudgeMapping = useCallback(async () => {
    if (!authToken) return;
    try {
      const { data } = await axios.get(`${API_BASE}/admin/mappings/project-judge`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      setProjectJudgeMapping(data.mappings || []);
    } catch (err) {
      console.error('Project-judge mapping load error', err);
    }
  }, [authToken]);

  const loadDetailedProjects = useCallback(async () => {
    if (!authToken) return;
    try {
      let url = `${API_BASE}/admin/projects/detailed`;
      const params = [];
      if (themeFilter) params.push(`theme=${themeFilter}`);
      if (statusFilter) params.push(`status=${statusFilter}`);
      if (params.length > 0) url += `?${params.join('&')}`;

      const { data } = await axios.get(url, {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      setDetailedProjects(data.projects || []);
    } catch (err) {
      console.error('Detailed projects load error', err);
    }
  }, [authToken, themeFilter, statusFilter]);

  const loadDetailedFaculty = useCallback(async () => {
    if (!authToken) return;
    try {
      const { data } = await axios.get(`${API_BASE}/admin/faculty/detailed`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      setDetailedFaculty(data.faculty || []);
    } catch (err) {
      console.error('Detailed faculty load error', err);
    }
  }, [authToken]);



  const loadThemes = useCallback(async () => {
    if (!authToken) return;
    try {
      const { data } = await axios.get(`${API_BASE}/themes`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      setThemes(data || []);
    } catch (err) {
      console.error('Themes load error', err);
    }
  }, [authToken]);

  const loadFaculties = useCallback(async () => {
    if (!authToken) return;
    try {
      const { data } = await axios.get(`${API_BASE}/admin/unassigned_faculty`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      setFaculties(data.faculty || []);
    } catch (err) {
      console.error('Faculties load error', err);
    }
  }, [authToken]);

  const loadAssignments = useCallback(async () => {
    if (!authToken) return;
    try {
      const { data } = await axios.get(`${API_BASE}/admin/faculty_theme_assignments`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      setAssignments(data.assignments || []);
    } catch (err) {
      console.error('Assignments load error', err);
    }
  }, [authToken]);


  const loadInsights = useCallback(async () => {
    if (!authToken) return;
    try {
      const { data } = await axios.get(`${API_BASE}/admin/insights`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      setInsights(data);
    } catch (err) {
      console.error('Insights load error', err);
    }
  }, [authToken]);

  const loadSubmissions = useCallback(async () => {
    if (!authToken) return;
    try {
      const { data } = await axios.get(`${API_BASE}/admin/submissions/all`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      setSubmissions(data.submissions || []);
    } catch (err) {
      console.error('Submissions load error', err);
    }
  }, [authToken]);

  const handlePlagiarismCheck = async () => {
    if (!selectedProjectForPlag) {
      setMessage('⚠️ Please select a submission');
      return;
    }
    setCheckingPlagiarism(true);
    setPlagiarismResult(null);
    try {
      const { data } = await axios.post(
        `${API_BASE}/admin/plagiarism/check`,
        { submission_id: selectedProjectForPlag },
        { headers: { Authorization: `Bearer ${authToken}` } }
      );
      setPlagiarismResult(data);
      setMessage(`✅ Plagiarism check completed: ${data.status}`);
    } catch (err) {
      setMessage(`❌ ${err.response?.data?.error || 'Plagiarism check failed'}`);
    } finally {
      setCheckingPlagiarism(false);
    }
  };

  useEffect(() => {
    if (!authToken) return;
    loadAnalytics();
    loadThemes();
    loadFaculties();
    loadAssignments();
    loadThemeDistribution();
    loadStudentMentorMapping();
    loadProjectJudgeMapping();
    loadDetailedProjects();
    loadDetailedFaculty();
    loadInsights();
    loadSubmissions();
  }, [authToken, loadAnalytics, loadThemes, loadFaculties, loadAssignments,
    loadThemeDistribution, loadStudentMentorMapping, loadProjectJudgeMapping,
    loadDetailedProjects, loadDetailedFaculty, loadInsights, loadSubmissions]);

  const handleAutoAssign = async () => {
    setAutoAssignLoading(true);
    setMessage('');
    try {
      const { data } = await axios.post(
        `${API_BASE}/admin/auto_assign`,
        {},
        { headers: { Authorization: `Bearer ${authToken}` } }
      );
      setMessage(`🤖 ${data.message}`);
      await loadFaculties();
      await loadAssignments();
      await loadAnalytics();
      await loadThemeDistribution();
    } catch (err) {
      setMessage(`❌ ${err.response?.data?.error || 'Auto-assignment failed'}`);
    } finally {
      setAutoAssignLoading(false);
    }
  };

  const handleManualAssign = async () => {
    if (!selectedFacultyId || !selectedThemeId) {
      setMessage('⚠️ Please select both faculty and theme');
      return;
    }
    try {
      await axios.post(
        `${API_BASE}/admin/assign_faculty_theme`,
        {
          FacultyUserID: selectedFacultyId,
          ThemeID: parseInt(selectedThemeId),
        },
        { headers: { Authorization: `Bearer ${authToken}` } }
      );
      setMessage('✅ Faculty assigned successfully');
      setSelectedFacultyId('');
      setSelectedThemeId('');
      await loadFaculties();
      await loadAssignments();
      await loadAnalytics();
    } catch (err) {
      setMessage(`❌ ${err.response?.data?.error || 'Assignment failed'}`);
    }
  };

  const handleUnassign = async (facultyId) => {
    if (!window.confirm('Are you sure you want to unassign this faculty?')) return;
    try {
      await axios.post(
        `${API_BASE}/admin/unassign_faculty_theme`,
        { FacultyUserID: facultyId },
        { headers: { Authorization: `Bearer ${authToken}` } }
      );
      setMessage('✅ Faculty unassigned successfully');
      await loadAssignments();
      await loadFaculties();
      await loadAnalytics();
      await loadThemeDistribution();
    } catch (err) {
      setMessage(`❌ ${err.response?.data?.error || 'Unassign failed'}`);
    }
  };

  const handleApprove = async (projectId) => {
    try {
      await approveProject(authToken, projectId);
      setMessage('✅ Project approved');
      loadDetailedProjects();
      loadAnalytics();
    } catch (err) {
      setMessage(`❌ ${err.response?.data?.error || 'Approval failed'}`);
    }
  };

  const handleReject = async (projectId) => {
    try {
      await rejectProject(authToken, projectId);
      setMessage('✅ Project rejected');
      loadDetailedProjects();
      loadAnalytics();
    } catch (err) {
      setMessage(`❌ ${err.response?.data?.error || 'Rejection failed'}`);
    }
  };

  const handleExportCSV = async () => {
    try {
      const response = await exportProjectsCSV(authToken);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'project_rankings.csv');
      document.body.appendChild(link);
      link.click();
      link.remove();
      setMessage('✅ CSV downloaded successfully');
    } catch (err) {
      setMessage('❌ Failed to export CSV');
    }
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    setCreatingUser(true);
    setMessage('');
    try {
      await axios.post(`${API_BASE}/auth/create_user`, {
        ...userForm,
        Dept: userForm.dept,
        Semester: userForm.semester
      }, {
        headers: { Authorization: `Bearer ${authToken}` }
      });
      setMessage('✅ User created successfully!');
      setUserForm({
        user_id: '',
        name: '',
        email: '',
        password: '',
        role: 'Student',
        dept: '',
        semester: ''
      });
      loadFaculties(); // Refresh faculty list if needed
    } catch (err) {
      setMessage(`❌ ${err.response?.data?.error || 'User creation failed'}`);
    } finally {
      setCreatingUser(false);
    }
  };

  const handleCreateTheme = async (e) => {
    e.preventDefault();
    setCreatingTheme(true);
    setMessage('');
    try {
      await axios.post(`${API_BASE}/themes`, themeForm, {
        headers: { Authorization: `Bearer ${authToken}` }
      });
      setMessage('✅ Theme created successfully!');
      setThemeForm({
        ThemeName: '',
        Description: '',
        MaxMentors: 5
      });
      loadThemes(); // Refresh themes list
    } catch (err) {
      setMessage(`❌ ${err.response?.data?.error || 'Theme creation failed'}`);
    } finally {
      setCreatingTheme(false);
    }
  };

  // Filter functions
  const filteredStudentMentor = studentMentorMapping.filter(m =>
    m.student_name.toLowerCase().includes(searchStudent.toLowerCase()) ||
    m.project_title.toLowerCase().includes(searchStudent.toLowerCase()) ||
    m.theme.toLowerCase().includes(searchStudent.toLowerCase()) ||
    m.mentor_name.toLowerCase().includes(searchStudent.toLowerCase())
  );

  const filteredProjects = detailedProjects.filter(p =>
    p.title.toLowerCase().includes(searchProject.toLowerCase()) ||
    p.theme_name.toLowerCase().includes(searchProject.toLowerCase()) ||
    p.team_members.toLowerCase().includes(searchProject.toLowerCase())
  );

  const filteredFaculty = detailedFaculty.filter(f =>
    f.name.toLowerCase().includes(searchFaculty.toLowerCase()) ||
    f.interests.toLowerCase().includes(searchFaculty.toLowerCase()) ||
    f.theme_name.toLowerCase().includes(searchFaculty.toLowerCase())
  );

  const filteredProjectJudge = projectJudgeMapping.filter(m =>
    m.project_title.toLowerCase().includes(searchTheme.toLowerCase()) ||
    m.theme.toLowerCase().includes(searchTheme.toLowerCase()) ||
    m.judge_name.toLowerCase().includes(searchTheme.toLowerCase())
  );

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, var(--color-bg) 0%, #0F172A 100%)' }}>
      {/* Clean Professional Header */}
      <div style={{
        background: 'var(--color-surface)',
        borderBottom: `2px solid var(--color-accent)`,
        padding: 'var(--space-lg) var(--space-2xl)',
      }}>
        <div style={{ maxWidth: '1600px', margin: '0 auto' }}>
          <h1 style={{
            fontSize: '1.75rem',
            fontWeight: 800,
            margin: 0,
            color: 'var(--color-text)',
          }}>
            <span style={{ color: 'var(--color-accent)' }}>RV College</span> · Experiential Learning Dashboard
          </h1>
          <p style={{ color: 'var(--color-text-dim)', margin: '0.25rem 0 0 0', fontSize: '0.875rem' }}>
            Administrator Analytics & Management Console
          </p>
        </div>
      </div>

      <div style={{
        padding: 'var(--space-2xl)',
        maxWidth: '1600px',
        margin: '0 auto',
      }}>
        {/* Message */}
        {message && (
          <div className={`alert ${message.includes('✅') ? 'alert-success' : message.includes('⚠️') ? 'alert-warning' : 'alert-error'}`}>
            {message}
          </div>
        )}

        {/* Tab Navigation */}
        <div style={{
          display: 'flex',
          gap: 'var(--space-sm)',
          marginBottom: 'var(--space-xl)',
          borderBottom: `2px solid var(--color-border)`,
          flexWrap: 'wrap',
        }}>
          {['insights', 'analytics', 'assignments', 'projects', 'mappings', 'faculty', 'management'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{
                padding: 'var(--space-md) var(--space-lg)',
                background: activeTab === tab ? 'var(--color-accent)' : 'transparent',
                border: 'none',
                borderBottom: `3px solid ${activeTab === tab ? 'var(--color-accent)' : 'transparent'}`,
                color: activeTab === tab ? 'white' : 'var(--color-text-dim)',
                fontWeight: 600,
                fontSize: '0.875rem',
                cursor: 'pointer',
                textTransform: 'capitalize',
                transition: 'all var(--transition-base)',
                borderRadius: activeTab === tab ? 'var(--radius-md) var(--radius-md) 0 0' : '0',
              }}
            >
              {tab}
            </button>
          ))}
        </div>

        {/* Insights Tab (Quick Win Feature) */}
        {activeTab === 'insights' && insights && (
          <div className="fade-in-up">
            {/* Top Stats */}
            <div className="grid grid-3" style={{ marginBottom: 'var(--space-2xl)' }}>
              <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
                <h4 style={{ color: 'var(--color-text)', marginBottom: 'var(--space-md)' }}>
                  Completion Rate
                </h4>
                <div style={{ fontSize: '3rem', fontWeight: 800, color: 'var(--color-accent)' }}>
                  {insights.completion_rate?.approval_rate || 0}%
                </div>
                <div style={{ color: 'var(--color-text-dim)', fontSize: '0.875rem' }}>
                  {insights.completion_rate?.approved || 0} / {insights.completion_rate?.total_projects || 0} approved
                </div>
              </div>

              <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
                <h4 style={{ color: 'var(--color-text)', marginBottom: 'var(--space-md)' }}>
                  At-Risk Projects
                </h4>
                <div style={{ fontSize: '3rem', fontWeight: 800, color: 'var(--color-error)' }}>
                  {insights.at_risk_projects?.length || 0}
                </div>
                <div style={{ color: 'var(--color-text-dim)', fontSize: '0.875rem' }}>
                  Need immediate attention
                </div>
              </div>

              <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
                <h4 style={{ color: 'var(--color-text)', marginBottom: 'var(--space-md)' }}>
                  Top Performer
                </h4>
                <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--color-success)' }}>
                  {insights.top_performers?.[0]?.name.split(' ')[0] || 'N/A'}
                </div>
                <div style={{ color: 'var(--color-text-dim)', fontSize: '0.875rem' }}>
                  Score: {insights.top_performers?.[0]?.avg_score || 0}/10
                </div>
              </div>
            </div>

            {/* Plagiarism Checker */}
            <div className="glass-card" style={{ padding: 'var(--space-xl)', marginBottom: 'var(--space-xl)' }}>
              <h3 style={{ marginBottom: 'var(--space-md)', color: 'var(--color-text)' }}>
                🔍 Plagiarism Detection (Submission-Based)
              </h3>
              <p style={{ color: 'var(--color-text-dim)', fontSize: '0.875rem', marginBottom: 'var(--space-md)' }}>
                Check student submissions for plagiarism. Supports both text content and URL-based submissions (Google Drive, GitHub, etc.)
              </p>
              <div style={{ display: 'flex', gap: 'var(--space-md)', alignItems: 'center', marginBottom: 'var(--space-lg)' }}>
                <select
                  value={selectedProjectForPlag}
                  onChange={(e) => setSelectedProjectForPlag(e.target.value)}
                  style={{ flex: 1 }}
                >
                  <option value="">Select Submission to Check</option>
                  {submissions.map(s => (
                    <option key={s.submission_id} value={s.submission_id}>
                      {s.is_url ? '🔗' : '📄'} {s.project_title} ({s.student_name}) - {s.content.substring(0, 30)}...
                    </option>
                  ))}
                </select>
                <button
                  onClick={handlePlagiarismCheck}
                  disabled={checkingPlagiarism || !selectedProjectForPlag}
                  className="btn btn-primary"
                >
                  {checkingPlagiarism ? 'Checking...' : 'Check Plagiarism'}
                </button>
              </div>


              {plagiarismResult && (
                <div>
                  <div style={{
                    padding: 'var(--space-lg)',
                    background: `var(--color-${plagiarismResult.color})`,
                    borderRadius: 'var(--radius-md)',
                    marginBottom: 'var(--space-lg)',
                    opacity: 0.15,
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div>
                        <h4 style={{ color: 'var(--color-text)', margin: 0 }}>
                          {plagiarismResult.project_title}
                        </h4>
                        <p style={{ color: 'var(--color-text-dim)', margin: '0.5rem 0 0 0', fontSize: '0.875rem' }}>
                          {plagiarismResult.is_url && <span className="badge badge-info" style={{ marginRight: 'var(--space-sm)' }}>🔗 URL Content</span>}
                          {plagiarismResult.submission_content}
                        </p>
                        <p style={{ color: 'var(--color-text-dim)', margin: '0.25rem 0 0 0', fontSize: '0.75rem' }}>
                          {plagiarismResult.message}
                        </p>
                      </div>
                      <div style={{ textAlign: 'right' }}>
                        <div style={{ fontSize: '2.5rem', fontWeight: 800, color: `var(--color-${plagiarismResult.color})` }}>
                          {plagiarismResult.plagiarism_score}%
                        </div>
                        <span className={`badge badge-${plagiarismResult.color}`}>
                          {plagiarismResult.status}
                        </span>
                      </div>
                    </div>
                  </div>

                  {plagiarismResult.matches && plagiarismResult.matches.length > 0 && (
                    <div>
                      <h4 style={{ marginBottom: 'var(--space-md)', color: 'var(--color-text)' }}>
                        Similar Submissions Found
                      </h4>
                      <div className="table-container">
                        <table className="table">
                          <thead>
                            <tr>
                              <th>Project</th>
                              <th>Content Preview</th>
                              <th>Similarity</th>
                              <th>Risk Level</th>
                            </tr>
                          </thead>
                          <tbody>
                            {plagiarismResult.matches.map((match, idx) => (
                              <tr key={idx}>
                                <td>{match.project_title}</td>
                                <td><small style={{ color: 'var(--color-text-dim)' }}>{match.content_preview}</small></td>
                                <td>
                                  <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)' }}>
                                    <div style={{
                                      width: '100px',
                                      height: '8px',
                                      background: 'var(--color-surface)',
                                      borderRadius: 'var(--radius-md)',
                                    }}>
                                      <div style={{
                                        width: `${match.similarity_score}%`,
                                        height: '100%',
                                        background: match.similarity_score > 60 ? 'var(--color-error)' : match.similarity_score > 30 ? 'var(--color-warning)' : 'var(--color-success)',
                                        borderRadius: 'var(--radius-md)',
                                      }} />
                                    </div>
                                    <span>{match.similarity_score}%</span>
                                  </div>
                                </td>
                                <td>
                                  <span className={`badge badge-${match.status === 'HIGH' ? 'error' : match.status === 'MEDIUM' ? 'warning' : 'success'}`}>
                                    {match.status}
                                  </span>
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Project Health */}
            <div className="grid grid-2" style={{ marginBottom: 'var(--space-xl)' }}>
              <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
                <h3 style={{ marginBottom: 'var(--space-lg)', color: 'var(--color-text)' }}>
                  🏥 Critical & At-Risk Projects
                </h3>
                <div className="table-container" style={{ maxHeight: '400px', overflowY: 'auto' }}>
                  <table className="table">
                    <thead>
                      <tr>
                        <th>Project</th>
                        <th>Health</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {insights.at_risk_projects?.map((project, idx) => (
                        <tr key={idx}>
                          <td>
                            <div>{project.title}</div>
                            <small className="badge badge-primary">{project.theme}</small>
                          </td>
                          <td>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)' }}>
                              <div style={{
                                width: '80px',
                                height: '8px',
                                background: 'var(--color-surface)',
                                borderRadius: 'var(--radius-md)',
                              }}>
                                <div style={{
                                  width: `${project.health_score}%`,
                                  height: '100%',
                                  background: `var(--color-${project.color})`,
                                  borderRadius: 'var(--radius-md)',
                                }} />
                              </div>
                              <span style={{ fontSize: '0.875rem' }}>{project.health_score}%</span>
                            </div>
                          </td>
                          <td>
                            <span className={`badge badge-${project.color}`}>
                              {project.health_status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
                <h3 style={{ marginBottom: 'var(--space-lg)', color: 'var(--color-text)' }}>
                  🏆 Top 10 Performers
                </h3>
                <div className="table-container" style={{ maxHeight: '400px', overflowY: 'auto' }}>
                  <table className="table">
                    <thead>
                      <tr>
                        <th>Rank</th>
                        <th>Student</th>
                        <th>Avg Score</th>
                      </tr>
                    </thead>
                    <tbody>
                      {insights.top_performers?.map((student, idx) => (
                        <tr key={idx}>
                          <td>
                            <span style={{
                              fontSize: '1.25rem',
                              fontWeight: 700,
                              color: idx === 0 ? 'gold' : idx === 1 ? 'silver' : idx === 2 ? '#CD7F32' : 'var(--color-text-dim)'
                            }}>
                              #{idx + 1}
                            </span>
                          </td>
                          <td>{student.name}</td>
                          <td>
                            <span style={{
                              fontSize: '1.125rem',
                              fontWeight: 700,
                              color: 'var(--color-success)'
                            }}>
                              {student.avg_score}/10
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            {/* Theme Popularity & Faculty Performance */}
            <div className="grid grid-2">
              <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
                <h3 style={{ marginBottom: 'var(--space-lg)', color: 'var(--color-text)' }}>
                  📈 Theme Popularity
                </h3>
                <PowerBIChart
                  title=""
                  type="bar"
                  data={insights.theme_popularity?.map(t => ({
                    label: t.theme,
                    value: t.project_count,
                  })) || []}
                />
              </div>

              <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
                <h3 style={{ marginBottom: 'var(--space-lg)', color: 'var(--color-text)' }}>
                  👨‍🏫 Top Faculty Mentors
                </h3>
                <div className="table-container" style={{ maxHeight: '400px', overflowY: 'auto' }}>
                  <table className="table">
                    <thead>
                      <tr>
                        <th>Faculty</th>
                        <th>Projects</th>
                        <th>Avg Score</th>
                      </tr>
                    </thead>
                    <tbody>
                      {insights.faculty_performance?.map((faculty, idx) => (
                        <tr key={idx}>
                          <td>{faculty.name}</td>
                          <td>{faculty.mentor_count}</td>
                          <td>
                            <span style={{ color: 'var(--color-accent)', fontWeight: 600 }}>
                              {faculty.avg_mentee_score}/10
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Analytics Tab with Power BI Style */}
        {activeTab === 'analytics' && analytics && (
          <div className="fade-in-up">
            <div className="grid grid-4" style={{ marginBottom: 'var(--space-2xl)' }}>
              <StatsWidget
                title="Total Projects"
                value={analytics.overall?.total_projects || 0}
                icon="📊"
                color="info"
              />
              <StatsWidget
                title="Total Faculty"
                value={analytics.overall?.total_faculty || 0}
                subtitle={`${analytics.overall?.assigned_faculty || 0} assigned`}
                icon="👨‍🏫"
                color="accent"
              />
              <StatsWidget
                title="Total Students"
                value={analytics.overall?.total_students || 0}
                icon="🎓"
                color="success"
              />
              <StatsWidget
                title="Themes"
                value={analytics.overall?.total_themes || 0}
                subtitle={`${analytics.overall?.unassigned_faculty || 0} faculty unassigned`}
                icon="🎯"
                color="warning"
              />
            </div>

            {/* Power BI Style Charts */}
            <div className="grid grid-3" style={{ marginBottom: 'var(--space-2xl)' }}>
              <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
                <PowerBIChart
                  title="Projects Distribution"
                  type="donut"
                  data={analytics.projects_by_theme?.map(item => ({
                    label: item.theme,
                    value: item.count,
                  })) || []}
                />
              </div>

              <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
                <PowerBIChart
                  title="Faculty Workload (Top 10)"
                  type="bar"
                  data={analytics.faculty_workload?.slice(0, 10).map(item => ({
                    label: item.name.split(' ')[0],
                    value: item.total,
                  })) || []}
                />
              </div>

              <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
                <PowerBIChart
                  title="Phase Scores"
                  type="bar"
                  data={analytics.avg_scores_by_phase?.map(item => ({
                    label: item.phase,
                    value: item.avg_score,
                  })) || []}
                />
              </div>
            </div>

            {/* Theme Distribution Table */}
            <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
              <h3 style={{ marginBottom: 'var(--space-lg)', color: 'var(--color-text)' }}>
                Theme Capacity Analysis
              </h3>
              <div className="table-container">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Theme</th>
                      <th>Faculty</th>
                      <th>Capacity</th>
                      <th>Projects</th>
                      <th>Approved</th>
                    </tr>
                  </thead>
                  <tbody>
                    {themeDistribution.map((theme, idx) => (
                      <tr key={idx}>
                        <td>{theme.theme_name}</td>
                        <td>{theme.assigned_faculty}</td>
                        <td>
                          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)' }}>
                            <span>{theme.capacity_used}</span>
                            <div style={{
                              width: '100px',
                              height: '8px',
                              background: 'var(--color-surface)',
                              borderRadius: 'var(--radius-md)',
                              overflow: 'hidden',
                            }}>
                              <div style={{
                                width: `${theme.capacity_percentage}%`,
                                height: '100%',
                                background: theme.capacity_percentage > 80 ? 'var(--color-error)' : 'var(--color-accent)',
                                transition: 'width 0.3s ease',
                              }} />
                            </div>
                            <span style={{ fontSize: '0.75rem', color: 'var(--color-text-dim)' }}>
                              {theme.capacity_percentage}%
                            </span>
                          </div>
                        </td>
                        <td>{theme.total_projects}</td>
                        <td>{theme.approved_projects}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Assignments Tab */}
        {activeTab === 'assignments' && (
          <div className="fade-in-up">
            <div className="glass-card" style={{ padding: 'var(--space-xl)', marginBottom: 'var(--space-xl)' }}>
              <h3 style={{ marginBottom: 'var(--space-md)', color: 'var(--color-text)' }}>
                🤖 AI-Powered Auto-Assignment (NLP-Based)
              </h3>
              <p style={{ color: 'var(--color-text-dim)', marginBottom: 'var(--space-lg)', fontSize: '0.875rem' }}>
                TF-IDF semantic similarity with synonym expansion
              </p>
              <button
                onClick={handleAutoAssign}
                disabled={autoAssignLoading}
                className="btn btn-primary"
                style={{ minWidth: '250px' }}
              >
                {autoAssignLoading ? (
                  <>
                    <div className="spinner" style={{ width: '20px', height: '20px', display: 'inline-block', marginRight: 'var(--space-sm)' }} />
                    Processing...
                  </>
                ) : (
                  '⚡ Run AI Auto-Assignment'
                )}
              </button>
            </div>

            <div className="glass-card" style={{ padding: 'var(--space-xl)', marginBottom: 'var(--space-xl)' }}>
              <h3 style={{ marginBottom: 'var(--space-md)', color: 'var(--color-text)' }}>
                Manual Assignment (Admin Override)
              </h3>
              <div className="grid grid-3" style={{ marginTop: 'var(--space-lg)' }}>
                <select
                  value={selectedFacultyId}
                  onChange={(e) => setSelectedFacultyId(e.target.value)}
                >
                  <option value="">Select Faculty</option>
                  {faculties.map(f => (
                    <option key={f.UserID} value={f.UserID}>
                      {f.Name} - {f.Interests?.substring(0, 30)}...
                    </option>
                  ))}
                </select>
                <select
                  value={selectedThemeId}
                  onChange={(e) => setSelectedThemeId(e.target.value)}
                >
                  <option value="">Select Theme</option>
                  {themes.map(t => (
                    <option key={t.ThemeID} value={t.ThemeID}>
                      {t.ThemeName}
                    </option>
                  ))}
                </select>
                <button onClick={handleManualAssign} className="btn btn-primary">
                  Assign
                </button>
              </div>
            </div>

            <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
              <h3 style={{ marginBottom: 'var(--space-lg)', color: 'var(--color-text)' }}>
                Current Assignments ({assignments.length})
              </h3>
              <div className="table-container">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Faculty</th>
                      <th>Theme</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {assignments.map((a, idx) => (
                      <tr key={idx}>
                        <td>{a.FacultyName}</td>
                        <td>
                          <span className="badge badge-primary">{a.ThemeName}</span>
                        </td>
                        <td>
                          <button
                            onClick={() => handleUnassign(a.FacultyUserID)}
                            className="btn"
                            style={{
                              padding: 'var(--space-xs) var(--space-sm)',
                              background: 'var(--color-error)',
                              fontSize: '0.75rem',
                              color: 'white'
                            }}
                          >
                            🗑️ Remove
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Projects Tab with Search */}
        {activeTab === 'projects' && (
          <div className="fade-in-up">
            <div style={{ marginBottom: 'var(--space-xl)', display: 'flex', gap: 'var(--space-md)', flexWrap: 'wrap', alignItems: 'center' }}>
              <SearchBar
                placeholder="Search projects, teams, themes..."
                value={searchProject}
                onChange={setSearchProject}
                onClear={() => setSearchProject('')}
              />
              <select value={themeFilter} onChange={(e) => setThemeFilter(e.target.value)}>
                <option value="">All Themes</option>
                {themes.map(t => (
                  <option key={t.ThemeID} value={t.ThemeID}>{t.ThemeName}</option>
                ))}
              </select>
              <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
                <option value="">All Status</option>
                <option value="Pending">Pending</option>
                <option value="Approved">Approved</option>
                <option value="Rejected">Rejected</option>
              </select>
              <button onClick={loadDetailedProjects} className="btn btn-secondary">
                Apply Filters
              </button>
              <button onClick={handleExportCSV} className="btn btn-primary">
                ⬇️ Export CSV
              </button>
            </div>

            <div className="glass-card">
              <div className="table-container">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Project</th>
                      <th>Theme</th>
                      <th>Team</th>
                      <th>Mentors</th>
                      <th>Judges</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredProjects.map(project => (
                      <tr key={project.project_id}>
                        <td>
                          <strong>{project.title}</strong>
                          <br />
                          <small style={{ color: 'var(--color-text-dim)' }}>ID: {project.project_id}</small>
                        </td>
                        <td>
                          <span className="badge badge-primary">{project.theme_name}</span>
                        </td>
                        <td>
                          <div>{project.team_size} members</div>
                          <small style={{ color: 'var(--color-text-dim)' }}>{project.team_members.substring(0, 30)}...</small>
                        </td>
                        <td><small>{project.mentors.substring(0, 30)}...</small></td>
                        <td><small>{project.judges.substring(0, 30)}...</small></td>
                        <td>
                          <span className={`badge ${project.status === 'Approved' ? 'badge-success' : project.status === 'Rejected' ? 'badge-error' : 'badge-warning'}`}>
                            {project.status}
                          </span>
                        </td>
                        <td>
                          <div style={{ display: 'flex', gap: 'var(--space-xs)' }}>
                            <button onClick={() => handleApprove(project.project_id)} className="btn btn-success" style={{ padding: '0.25rem 0.75rem', fontSize: '0.75rem' }}>
                              Approve
                            </button>
                            <button onClick={() => handleReject(project.project_id)} className="btn btn-danger" style={{ padding: '0.25rem 0.75rem', fontSize: '0.75rem' }}>
                              Reject
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {filteredProjects.length === 0 && (
                  <div style={{ padding: 'var(--space-2xl)', textAlign: 'center', color: 'var(--color-text-dim)' }}>
                    No projects found matching your search
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Mappings Tab with Search */}
        {activeTab === 'mappings' && (
          <div className="fade-in-up">
            <div className="grid grid-2" style={{ marginBottom: 'var(--space-xl)' }}>
              <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
                <div style={{ marginBottom: 'var(--space-lg)' }}>
                  <h3 style={{ marginBottom: 'var(--space-md)', color: 'var(--color-text)' }}>
                    Student-Mentor Mapping ({filteredStudentMentor.length})
                  </h3>
                  <SearchBar
                    placeholder="Search students, projects, mentors..."
                    value={searchStudent}
                    onChange={setSearchStudent}
                    onClear={() => setSearchStudent('')}
                  />
                </div>
                <div className="table-container" style={{ maxHeight: '500px', overflowY: 'auto' }}>
                  <table className="table">
                    <thead>
                      <tr>
                        <th>Student</th>
                        <th>Project</th>
                        <th>Mentor</th>
                      </tr>
                    </thead>
                    <tbody>
                      {filteredStudentMentor.map((mapping, idx) => (
                        <tr key={idx}>
                          <td>{mapping.student_name}</td>
                          <td>
                            <div>{mapping.project_title}</div>
                            <small className="badge badge-primary">{mapping.theme}</small>
                          </td>
                          <td>{mapping.mentor_name}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {filteredStudentMentor.length === 0 && (
                    <div style={{ padding: 'var(--space-xl)', textAlign: 'center', color: 'var(--color-text-dim)' }}>
                      No results found
                    </div>
                  )}
                </div>
              </div>

              <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
                <div style={{ marginBottom: 'var(--space-lg)' }}>
                  <h3 style={{ marginBottom: 'var(--space-md)', color: 'var(--color-text)' }}>
                    Project-Judge Mapping ({filteredProjectJudge.length})
                  </h3>
                  <SearchBar
                    placeholder="Search projects, themes, judges..."
                    value={searchTheme}
                    onChange={setSearchTheme}
                    onClear={() => setSearchTheme('')}
                  />
                </div>
                <div className="table-container" style={{ maxHeight: '500px', overflowY: 'auto' }}>
                  <table className="table">
                    <thead>
                      <tr>
                        <th>Project</th>
                        <th>Judge</th>
                        <th>Type</th>
                      </tr>
                    </thead>
                    <tbody>
                      {filteredProjectJudge.map((mapping, idx) => (
                        <tr key={idx}>
                          <td>
                            <div>{mapping.project_title}</div>
                            <small className="badge badge-primary">{mapping.theme}</small>
                          </td>
                          <td>{mapping.judge_name}</td>
                          <td>
                            <span className="badge badge-success">{mapping.selection_type}</span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {filteredProjectJudge.length === 0 && (
                    <div style={{ padding: 'var(--space-xl)', textAlign: 'center', color: 'var(--color-text-dim)' }}>
                      No results found
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Faculty Tab with Search */}
        {activeTab === 'faculty' && (
          <div className="fade-in-up">
            <div style={{ marginBottom: 'var(--space-lg)' }}>
              <SearchBar
                placeholder="Search faculty by name, interests, or theme..."
                value={searchFaculty}
                onChange={setSearchFaculty}
                onClear={() => setSearchFaculty('')}
              />
            </div>

            <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
              <h3 style={{ marginBottom: 'var(--space-lg)', color: 'var(--color-text)' }}>
                Faculty Details & Workload ({filteredFaculty.length})
              </h3>
              <div className="table-container">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Faculty</th>
                      <th>Department</th>
                      <th>Interests</th>
                      <th>Theme</th>
                      <th>Mentoring</th>
                      <th>Judging</th>
                      <th>Total Load</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredFaculty.map((faculty, idx) => (
                      <tr key={idx}>
                        <td>
                          <div>{faculty.name}</div>
                          <small style={{ color: 'var(--color-text-dim)' }}>{faculty.email}</small>
                        </td>
                        <td>{faculty.department}</td>
                        <td>
                          <small style={{ color: 'var(--color-text-dim)' }}>
                            {faculty.interests.substring(0, 30)}...
                          </small>
                        </td>
                        <td>
                          <span className="badge badge-primary">{faculty.theme_name}</span>
                        </td>
                        <td>{faculty.mentor_count}</td>
                        <td>{faculty.judge_count}</td>
                        <td>
                          <span className={`badge ${faculty.total_load > 8 ? 'badge-error' : faculty.total_load > 5 ? 'badge-warning' : 'badge-success'}`}>
                            {faculty.total_load}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {filteredFaculty.length === 0 && (
                  <div style={{ padding: 'var(--space-2xl)', textAlign: 'center', color: 'var(--color-text-dim)' }}>
                    No faculty found matching your search
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Management Tab */}
        {activeTab === 'management' && (
          <div className="fade-in-up">
            <div className="grid grid-2">
              {/* Create User Form */}
              <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
                <h3 style={{ marginBottom: 'var(--space-lg)', color: 'var(--color-text)' }}>
                  👤 Create New User
                </h3>
                <form onSubmit={handleCreateUser}>
                  <div style={{ marginBottom: 'var(--space-md)' }}>
                    <label style={{ display: 'block', marginBottom: 'var(--space-xs)' }}>User ID (USN/ID)</label>
                    <input
                      type="text"
                      value={userForm.user_id}
                      onChange={(e) => setUserForm({ ...userForm, user_id: e.target.value })}
                      placeholder="e.g., 1RV21CS001"
                      required
                    />
                  </div>
                  <div className="grid grid-2" style={{ marginBottom: 'var(--space-md)' }}>
                    <div>
                      <label style={{ display: 'block', marginBottom: 'var(--space-xs)' }}>Full Name</label>
                      <input
                        type="text"
                        value={userForm.name}
                        onChange={(e) => setUserForm({ ...userForm, name: e.target.value })}
                        required
                      />
                    </div>
                    <div>
                      <label style={{ display: 'block', marginBottom: 'var(--space-xs)' }}>Email</label>
                      <input
                        type="email"
                        value={userForm.email}
                        onChange={(e) => setUserForm({ ...userForm, email: e.target.value })}
                        required
                      />
                    </div>
                  </div>
                  <div className="grid grid-2" style={{ marginBottom: 'var(--space-md)' }}>
                    <div>
                      <label style={{ display: 'block', marginBottom: 'var(--space-xs)' }}>Password</label>
                      <input
                        type="password"
                        value={userForm.password}
                        onChange={(e) => setUserForm({ ...userForm, password: e.target.value })}
                        required
                      />
                    </div>
                    <div>
                      <label style={{ display: 'block', marginBottom: 'var(--space-xs)' }}>Role</label>
                      <select
                        value={userForm.role}
                        onChange={(e) => setUserForm({ ...userForm, role: e.target.value })}
                      >
                        <option value="Student">Student</option>
                        <option value="Faculty">Faculty</option>
                        <option value="Admin">Admin</option>
                      </select>
                    </div>
                  </div>
                  <div className="grid grid-2" style={{ marginBottom: 'var(--space-lg)' }}>
                    <div>
                      <label style={{ display: 'block', marginBottom: 'var(--space-xs)' }}>Department</label>
                      <input
                        type="text"
                        value={userForm.dept}
                        onChange={(e) => setUserForm({ ...userForm, dept: e.target.value })}
                        placeholder="e.g., CS"
                        required
                      />
                    </div>
                    {userForm.role === 'Student' && (
                      <div>
                        <label style={{ display: 'block', marginBottom: 'var(--space-xs)' }}>Semester</label>
                        <input
                          type="number"
                          value={userForm.semester}
                          onChange={(e) => setUserForm({ ...userForm, semester: e.target.value })}
                          required
                        />
                      </div>
                    )}
                  </div>
                  <button type="submit" disabled={creatingUser} className="btn btn-primary" style={{ width: '100%' }}>
                    {creatingUser ? 'Creating...' : 'Create User'}
                  </button>
                </form>
              </div>

              {/* Create Theme Form */}
              <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
                <h3 style={{ marginBottom: 'var(--space-lg)', color: 'var(--color-text)' }}>
                  🎯 Create New Theme
                </h3>
                <form onSubmit={handleCreateTheme}>
                  <div style={{ marginBottom: 'var(--space-md)' }}>
                    <label style={{ display: 'block', marginBottom: 'var(--space-xs)' }}>Theme Name</label>
                    <input
                      type="text"
                      value={themeForm.ThemeName}
                      onChange={(e) => setThemeForm({ ...themeForm, ThemeName: e.target.value })}
                      placeholder="e.g., Blockchain Applications"
                      required
                    />
                  </div>
                  <div style={{ marginBottom: 'var(--space-md)' }}>
                    <label style={{ display: 'block', marginBottom: 'var(--space-xs)' }}>Description</label>
                    <textarea
                      value={themeForm.Description}
                      onChange={(e) => setThemeForm({ ...themeForm, Description: e.target.value })}
                      rows={4}
                      placeholder="Describe the theme scope..."
                      required
                    />
                  </div>
                  <div style={{ marginBottom: 'var(--space-lg)' }}>
                    <label style={{ display: 'block', marginBottom: 'var(--space-xs)' }}>Max Mentors</label>
                    <input
                      type="number"
                      value={themeForm.MaxMentors}
                      onChange={(e) => setThemeForm({ ...themeForm, MaxMentors: parseInt(e.target.value) })}
                      required
                    />
                  </div>
                  <button type="submit" disabled={creatingTheme} className="btn btn-accent" style={{ width: '100%' }}>
                    {creatingTheme ? 'Creating...' : 'Create Theme'}
                  </button>
                </form>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default AdminDashboard;
