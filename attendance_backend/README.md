# Attendance Backend (Global Levels) - Django + DRF + Admin

## Setup
```bash
cd attendance_backend
python -m venv venv
source venv/bin/activate   # windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

Admin:
- http://127.0.0.1:8000/admin/

JWT:
- POST /api/auth/token/  {"username":"...","password":"..."}

Core:
- GET /api/branches/
- GET /api/levels/                       (global)
- GET /api/batches/?branch_id=1&level_id=1&is_active=true
- GET /api/batches/1/students/

Attendance:
- POST /api/attendance/sessions/  {"batch":1,"date":"2026-02-22","label":"Daily"}
- PUT  /api/attendance/sessions/{id}/marks/  {"marks":[{"student":1,"status":"P"}]}
