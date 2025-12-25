import axios from 'axios';

const API_BASE = 'http://127.0.0.1:5000';

export function getSubmissionsByProject(token, projectId) {
  return axios.get(`${API_BASE}/submissions/project/${projectId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}
