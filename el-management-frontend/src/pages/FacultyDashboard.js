import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import {
  getMyTheme,
  getAvailableProjects,
  selfAssignMentor,
  selfAssignJudge,
  getMyMentorAssignments,
  getMyJudgeAssignments,
  getProjectDetailsWithSubmissions,
  submitEvaluation,
  getProjectTeamMembers,
  getProjectPhaseAggregate,
} from '../api/faculty';
import axios from 'axios';
const API_BASE = 'http://localhost:5000';

function FacultyDashboard() {
  const { authToken } = useAuth();

  const [myTheme, setMyTheme] = useState(null);
  const [interests, setInterests] = useState('');
  const [showInterestsEditor, setShowInterestsEditor] = useState(false);
  const [availableProjects, setAvailableProjects] = useState([]);
  const [mentorAssignments, setMentorAssignments] = useState([]);
  const [judgeAssignments, setJudgeAssignments] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [selectedSubs, setSelectedSubs] = useState([]);
  const [teamMembers, setTeamMembers] = useState([]);
  const [evaluations, setEvaluations] = useState([]);
  const [phaseAggregates, setPhaseAggregates] = useState({});
  const [message, setMessage] = useState('');

  const [showEvalForm, setShowEvalForm] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [evalData, setEvalData] = useState({ score: '', feedback: '', phase: 'Phase1' });

  useEffect(() => {
    if (!authToken) return;
    Promise.all([
      getMyTheme(authToken).then(res => setMyTheme(res.data)).catch(() => setMyTheme(null)),
      getAvailableProjects(authToken).then(res => setAvailableProjects(res.data)).catch(() => setAvailableProjects([])),
      getMyMentorAssignments(authToken).then(res => setMentorAssignments(res.data)).catch(() => setMentorAssignments([])),
      getMyJudgeAssignments(authToken).then(res => setJudgeAssignments(res.data)).catch(() => setJudgeAssignments([])),
      axios.get(`${API_BASE}/auth/faculty/profile`, {
        headers: { Authorization: `Bearer ${authToken}` }
      }).then(res => setInterests(res.data.interests || '')).catch(() => { }),
    ]);
  }, [authToken]);

  const refreshAssignments = async () => {
    const [mentorsRes, judgesRes] = await Promise.all([
      getMyMentorAssignments(authToken),
      getMyJudgeAssignments(authToken),
    ]);
    setMentorAssignments(mentorsRes.data);
    setJudgeAssignments(judgesRes.data);
  };

  const handleUpdateInterests = async () => {
    try {
      await axios.put(
        `${API_BASE}/auth/faculty/interests`,
        { interests },
        { headers: { Authorization: `Bearer ${authToken}` } }
      );
      setMessage('✅ Interests updated successfully!');
      setShowInterestsEditor(false);
    } catch (err) {
      setMessage(`❌ ${err.response?.data?.error || 'Update failed'}`);
    }
  };

  const handleMentor = async (projectId) => {
    setMessage('');
    try {
      const res = await selfAssignMentor(authToken, projectId);
      setMessage(`✅ ${res.data.message}`);
      await refreshAssignments();
    } catch (err) {
      setMessage(`❌ ${err.response?.data?.error || 'Mentor failed'}`);
    }
  };

  const handleJudge = async (projectId) => {
    setMessage('');
    try {
      const res = await selfAssignJudge(authToken, projectId);
      setMessage(`✅ ${res.data.message}`);
      await refreshAssignments();
    } catch (err) {
      setMessage(`❌ ${err.response?.data?.error || 'Judge failed'}`);
    }
  };

  const handleViewDetails = async (projectId) => {
    setMessage('');
    setSelectedProject(null);
    setSelectedSubs([]);
    setTeamMembers([]);
    setEvaluations([]);
    setPhaseAggregates({});

    try {
      const detailsRes = await getProjectDetailsWithSubmissions(authToken, projectId);
      setSelectedProject(detailsRes.data.project);
      setSelectedSubs(detailsRes.data.submissions || []);
      setEvaluations(detailsRes.data.evaluations || []);

      const teamRes = await getProjectTeamMembers(authToken, projectId);
      setTeamMembers(teamRes.data || []);

      const aggregates = {};
      for (const phase of ['Phase1', 'Phase2', 'Phase3']) {
        try {
          const aggRes = await getProjectPhaseAggregate(authToken, projectId, phase);
          aggregates[phase] = aggRes.data;
        } catch (e) { /* ignore */ }
      }
      setPhaseAggregates(aggregates);
    } catch (err) {
      setMessage(`❌ ${err.response?.data?.error || 'Load failed'}`);
    }
  };

  const isJudgeForProject = () => judgeAssignments.some(a => a.ProjectID === selectedProject?.ProjectID);

  const getNextPhaseForStudent = (studentId) => {
    const studentEvals = evaluations.filter(e => e.StudentUserID === studentId);
    const phases = ['Phase1', 'Phase2', 'Phase3'];
    for (const phase of phases) {
      if (!studentEvals.some(e => e.Phase === phase)) return phase;
    }
    return null;
  };

  const handleSelectStudent = (student) => {
    setSelectedStudent(student);
    setEvalData({
      score: '',
      feedback: '',
      phase: getNextPhaseForStudent(student.UserID) || 'Phase1'
    });
    setShowEvalForm(true);
  };

  const handleSubmitEval = async (e) => {
    e.preventDefault();
    if (!selectedStudent) return; // Removed '!evalData.score' check to allow Mentors (Feedback only)

    try {
      await submitEvaluation(authToken, selectedProject.ProjectID, {
        Score: evalData.score,
        Feedback: evalData.feedback,
        Phase: evalData.phase,
        StudentUserID: selectedStudent.UserID,
      });
      setMessage(`✅ ${selectedStudent.UserName} evaluation submitted!`);
      setShowEvalForm(false);
      await handleViewDetails(selectedProject.ProjectID);
    } catch (err) {
      setMessage(`❌ ${err.response?.data?.error || 'Submit failed'}`);
    }
  };

  return (
    <div style={{
      padding: 'var(--space-2xl)',
      maxWidth: '1400px',
      margin: '0 auto',
      minHeight: '100vh',
    }}>
      {/* Header */}
      <div style={{ marginBottom: 'var(--space-2xl)' }}>
        <h1 style={{
          fontSize: '2.5rem',
          fontWeight: 800,
          margin: 0,
          marginBottom: 'var(--space-sm)',
        }} className="text-gradient">
          Faculty Dashboard
        </h1>
        {myTheme && (
          <p style={{ color: 'var(--color-text-dim)', margin: 0 }}>
            Your theme: <span style={{ color: 'var(--color-accent)', fontWeight: 600 }}>{myTheme.ThemeName}</span>
          </p>
        )}
      </div>

      {/* Message */}
      {message && (
        <div className={`alert ${message.includes('✅') ? 'alert-success' : 'alert-error'}`}>
          {message}
        </div>
      )}

      {/* Interests Section */}
      <div className="glass-card fade-in-up" style={{ padding: 'var(--space-xl)', marginBottom: 'var(--space-xl)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-md)' }}>
          <h3 style={{ margin: 0, color: 'var(--color-text)' }}>🎯 Your Interests</h3>
          <button
            onClick={() => setShowInterestsEditor(!showInterestsEditor)}
            className="btn btn-secondary"
          >
            {showInterestsEditor ? 'Cancel' : 'Edit'}
          </button>
        </div>

        {showInterestsEditor ? (
          <div>
            <textarea
              value={interests}
              onChange={(e) => setInterests(e.target.value)}
              placeholder="e.g., Machine Learning, AI, IoT, Blockchain (comma-separated)"
              rows={3}
              style={{ marginBottom: 'var(--space-md)' }}
            />
            <button onClick={handleUpdateInterests} className="btn btn-primary">
              Save Interests
            </button>
          </div>
        ) : (
          <p style={{ color: 'var(--color-text-dim)', margin: 0 }}>
            {interests || 'No interests set yet. Click Edit to add your areas of interest for better theme matching.'}
          </p>
        )}
      </div>

      {/* Stats Grid */}
      <div className="grid grid-3" style={{ marginBottom: 'var(--space-2xl)' }}>
        <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
          <div style={{ fontSize: '2rem', marginBottom: 'var(--space-sm)' }}>📝</div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--color-accent)' }}>
            {availableProjects.length}
          </div>
          <div style={{ color: 'var(--color-text-dim)', fontSize: '0.875rem' }}>
            Available Projects
          </div>
        </div>

        <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
          <div style={{ fontSize: '2rem', marginBottom: 'var(--space-sm)' }}>👨‍🏫</div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--color-success)' }}>
            {mentorAssignments.length}
          </div>
          <div style={{ color: 'var(--color-text-dim)', fontSize: '0.875rem' }}>
            Mentor Assignments
          </div>
        </div>

        <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
          <div style={{ fontSize: '2rem', marginBottom: 'var(--space-sm)' }}>⚖️</div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--color-info)' }}>
            {judgeAssignments.length}
          </div>
          <div style={{ color: 'var(--color-text-dim)', fontSize: '0.875rem' }}>
            Judge Assignments
          </div>
        </div>
      </div>

      {/* Your Assignments */}
      <div className="grid grid-2" style={{ marginBottom: 'var(--space-xl)' }}>
        {/* Mentor Assignments */}
        <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
          <h3 style={{ marginBottom: 'var(--space-lg)', color: 'var(--color-text)' }}>
            Your Mentor Assignments
          </h3>
          {mentorAssignments.length === 0 ? (
            <p style={{ color: 'var(--color-text-dim)' }}>No mentor assignments yet</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
              {mentorAssignments.map(a => (
                <div
                  key={a.ProjectID}
                  onClick={() => handleViewDetails(a.ProjectID)}
                  style={{
                    padding: 'var(--space-md)',
                    background: 'var(--color-surface)',
                    borderRadius: 'var(--radius-md)',
                    cursor: 'pointer',
                    borderLeft: '4px solid var(--color-success)',
                    transition: 'transform 0.2s',
                  }}
                  onMouseOver={(e) => e.currentTarget.style.transform = 'translateX(5px)'}
                  onMouseOut={(e) => e.currentTarget.style.transform = 'translateX(0)'}
                >
                  <div style={{ fontWeight: 600, color: 'var(--color-text)' }}>{a.Title}</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--color-text-dim)' }}>ID: {a.ProjectID} | Status: {a.Status}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Judge Assignments */}
        <div className="glass-card" style={{ padding: 'var(--space-xl)' }}>
          <h3 style={{ marginBottom: 'var(--space-lg)', color: 'var(--color-text)' }}>
            Your Judge Assignments
          </h3>
          {judgeAssignments.length === 0 ? (
            <p style={{ color: 'var(--color-text-dim)' }}>No judge assignments yet</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
              {judgeAssignments.map(a => (
                <div
                  key={a.ProjectID}
                  onClick={() => handleViewDetails(a.ProjectID)}
                  style={{
                    padding: 'var(--space-md)',
                    background: 'var(--color-surface)',
                    borderRadius: 'var(--radius-md)',
                    cursor: 'pointer',
                    borderLeft: '4px solid var(--color-info)',
                    transition: 'transform 0.2s',
                  }}
                  onMouseOver={(e) => e.currentTarget.style.transform = 'translateX(5px)'}
                  onMouseOut={(e) => e.currentTarget.style.transform = 'translateX(0)'}
                >
                  <div style={{ fontWeight: 600, color: 'var(--color-text)' }}>{a.Title}</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--color-text-dim)' }}>ID: {a.ProjectID} | Status: {a.Status}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Projects List */}
      <div className="glass-card" style={{ padding: 'var(--space-xl)', marginBottom: 'var(--space-xl)' }}>
        <h3 style={{ marginBottom: 'var(--space-lg)', color: 'var(--color-text)' }}>
          Projects in {myTheme ? <span style={{ color: 'var(--color-accent)' }}>{myTheme.ThemeName}</span> : 'Your Theme'}
        </h3>
        {availableProjects.length === 0 ? (
          <p style={{ color: 'var(--color-text-dim)' }}>No projects available</p>
        ) : (
          <div className="grid">
            {availableProjects.map(p => (
              <div key={p.ProjectID} className="glass-card" style={{ padding: 'var(--space-lg)' }}>
                <h4 style={{ marginBottom: 'var(--space-sm)', color: 'var(--color-accent)' }}>
                  {p.Title}
                </h4>
                <p style={{ color: 'var(--color-text-dim)', fontSize: '0.875rem', marginBottom: 'var(--space-md)' }}>
                  ID: {p.ProjectID} | Status: {p.Status}
                </p>
                {/* Status Indicators */}
                <div style={{ display: 'flex', gap: 'var(--space-xs)', marginBottom: 'var(--space-sm)' }}>
                  {mentorAssignments.some(a => a.ProjectID === p.ProjectID) && (
                    <span className="badge badge-success">Your Mentee</span>
                  )}
                  {judgeAssignments.some(a => a.ProjectID === p.ProjectID) && (
                    <span className="badge badge-info">Your Judge</span>
                  )}
                </div>
                <div style={{ display: 'flex', gap: 'var(--space-sm)' }}>
                  <button
                    onClick={() => handleMentor(p.ProjectID)}
                    disabled={mentorAssignments.some(a => a.ProjectID === p.ProjectID) || judgeAssignments.some(a => a.ProjectID === p.ProjectID)}
                    className="btn btn-success"
                  >
                    {mentorAssignments.some(a => a.ProjectID === p.ProjectID) ? 'Already Mentor' : 'Be Mentor'}
                  </button>
                  <button
                    onClick={() => handleJudge(p.ProjectID)}
                    disabled={judgeAssignments.some(a => a.ProjectID === p.ProjectID) || mentorAssignments.some(a => a.ProjectID === p.ProjectID)}
                    className="btn btn-primary"
                  >
                    {judgeAssignments.some(a => a.ProjectID === p.ProjectID) ? 'Already Judge' : 'Be Judge'}
                  </button>
                  <button onClick={() => handleViewDetails(p.ProjectID)} className="btn btn-secondary">
                    View Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Project Details */}
      {selectedProject && (
        <div className="glass-card fade-in-up" style={{ padding: 'var(--space-xl)' }}>
          <h3 style={{ marginBottom: 'var(--space-md)', color: 'var(--color-text)' }}>
            {selectedProject.Title}
          </h3>
          <p style={{ color: 'var(--color-text-dim)', marginBottom: 'var(--space-xl)' }}>
            Theme: {selectedProject.ThemeName} | Status: {selectedProject.Status}
          </p>

          {/* Phase Averages */}
          <h4 style={{ marginBottom: 'var(--space-md)', color: 'var(--color-text)' }}>Phase Averages</h4>
          <div className="grid grid-3" style={{ marginBottom: 'var(--space-xl)' }}>
            {['Phase1', 'Phase2', 'Phase3'].map(phase => {
              const agg = phaseAggregates[phase];
              return (
                <div key={phase} style={{
                  background: 'var(--color-surface)',
                  padding: 'var(--space-md)',
                  borderRadius: 'var(--radius-md)',
                }}>
                  <div style={{ fontSize: '0.875rem', color: 'var(--color-text-dim)', marginBottom: 'var(--space-xs)' }}>
                    {phase}
                  </div>
                  <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--color-accent)' }}>
                    {agg?.aggregate_score?.toFixed(1) ?? '—'}
                  </div>
                  <div style={{ fontSize: '0.875rem', color: 'var(--color-text-dim)' }}>
                    {agg?.students_scored ?? 0}/{teamMembers.length} scored
                  </div>
                </div>
              );
            })}
          </div>

          {/* Team Members */}
          <h4 style={{ marginBottom: 'var(--space-md)', color: 'var(--color-text)' }}>
            Team Members ({teamMembers.length})
          </h4>
          {teamMembers.map(student => {
            const studentEvals = evaluations.filter(e => e.StudentUserID === student.UserID);
            return (
              <div key={student.UserID} style={{
                background: 'var(--color-surface)',
                padding: 'var(--space-md)',
                borderRadius: 'var(--radius-md)',
                marginBottom: 'var(--space-sm)',
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <strong style={{ color: 'var(--color-text)' }}>
                    {student.UserName} ({student.UserID})
                  </strong>
                  <button
                    onClick={() => handleSelectStudent(student)}
                    disabled={!isJudgeForProject()}
                    className={isJudgeForProject() ? 'btn btn-success' : 'btn btn-secondary'}
                    style={{ padding: '0.5rem 1rem' }}
                  >
                    {getNextPhaseForStudent(student.UserID)
                      ? `Score ${getNextPhaseForStudent(student.UserID)}`
                      : '✅ Complete'
                    }
                  </button>
                </div>
                <div style={{ fontSize: '0.875rem', color: 'var(--color-text-dim)', marginTop: 'var(--space-sm)' }}>
                  {studentEvals.length > 0 ? studentEvals.map(ev => (
                    <div key={ev.EvaluationID}>{ev.Phase}: {ev.Score}/10</div>
                  )) : 'No scores yet'}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Eval Form Modal */}
      {showEvalForm && selectedStudent && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0, 0, 0, 0.8)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
        }}>
          <div className="glass-card" style={{
            padding: 'var(--space-2xl)',
            maxWidth: '500px',
            width: '90%',
          }}>
            <h3 style={{ marginBottom: 'var(--space-lg)', color: 'var(--color-text)' }}>
              Score {selectedStudent.UserName}
            </h3>
            <form onSubmit={handleSubmitEval}>
              <div style={{ marginBottom: 'var(--space-md)' }}>
                <label style={{ display: 'block', marginBottom: 'var(--space-xs)', color: 'var(--color-text)' }}>
                  Phase
                </label>
                <select
                  value={evalData.phase}
                  onChange={(e) => setEvalData({ ...evalData, phase: e.target.value })}
                >
                  <option value="Phase1">Phase 1</option>
                  <option value="Phase2">Phase 2</option>
                  <option value="Phase3">Phase 3</option>
                </select>
              </div>
              {/* Only Judges can Score */}
              {isJudgeForProject() && (
                <div style={{ marginBottom: 'var(--space-md)' }}>
                  <label style={{ display: 'block', marginBottom: 'var(--space-xs)', color: 'var(--color-text)' }}>
                    Score (0-10)
                  </label>
                  <input
                    type="number"
                    min="0"
                    max="10"
                    step="0.1"
                    value={evalData.score}
                    onChange={(e) => setEvalData({ ...evalData, score: e.target.value })}
                    required
                  />
                </div>
              )}
              <div style={{ marginBottom: 'var(--space-lg)' }}>
                <label style={{ display: 'block', marginBottom: 'var(--space-xs)', color: 'var(--color-text)' }}>
                  Feedback
                </label>
                <textarea
                  value={evalData.feedback}
                  onChange={(e) => setEvalData({ ...evalData, feedback: e.target.value })}
                  rows={3}
                />
              </div>
              <div style={{ display: 'flex', gap: 'var(--space-md)' }}>
                <button type="submit" className="btn btn-primary" style={{ flex: 1 }}>
                  Submit
                </button>
                <button
                  type="button"
                  onClick={() => setShowEvalForm(false)}
                  className="btn btn-secondary"
                  style={{ flex: 1 }}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default FacultyDashboard;
