const API_BASE = 'http://127.0.0.1:8000/api';

const AUTH_HEADER = {
  Authorization: 'Basic REPLACE_WITH_BASE64_CREDENTIALS'
};

export async function fetchStudents() {
  const response = await fetch(`${API_BASE}/students/`, { headers: AUTH_HEADER });
  if (!response.ok) throw new Error('Unable to load students');
  return response.json();
}

export async function createAttendance(payload) {
  const response = await fetch(`${API_BASE}/attendance/`, {
    method: 'POST',
    headers: { ...AUTH_HEADER, 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!response.ok) throw new Error('Unable to save attendance');
  return response.json();
}
