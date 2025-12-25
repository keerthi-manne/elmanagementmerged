import axios from 'axios';

const API_BASE = 'http://127.0.0.1:5000';

export function sendNotification(token, payload) {
  return axios.post(`${API_BASE}/notifications`, payload, {
    headers: { Authorization: `Bearer ${token}` },
  });
}
