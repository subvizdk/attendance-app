# Student Attendance App (Django + React Native)

This repository includes:
- `backend/`: Django + Django REST Framework backend with Django admin support.
- `mobile/`: React Native (Expo) app to record attendance.

## Domain Model
- **Branch**: Institution branch (city-specific).
- **Level**: Academic level under a branch.
- **Batch**: Group/cohort under a level for an academic year.
- **Student**: Assigned to exactly one current batch.
- **AttendanceRecord**: One attendance entry per student per date.

The data model supports creating new batches every year while preserving old attendance records.

## Backend Setup (Django)
1. Create virtualenv and install requirements:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Apply migrations and create admin user:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```
3. Run server:
   ```bash
   python manage.py runserver
   ```

### API Endpoints
- `GET /api/batches/`
- `GET /api/students/`
- `GET|POST|PUT|PATCH|DELETE /api/attendance/`

Authentication is currently Session/Basic auth. This is enough to launch quickly and can later be migrated to token-based auth.

## Admin Workflow
Use Django admin (`/admin`) to manage branches, levels, batches, students, and attendance.

## Mobile Setup (React Native)
1. Install dependencies:
   ```bash
   cd mobile
   npm install
   ```
2. Update `mobile/src/api/client.js`:
   - Set `API_BASE` to your backend host.
   - Replace `Authorization` placeholder with valid credentials (or move to token auth later).
3. Start app:
   ```bash
   npm run android
   ```

## Suggested Next Features
- Role-based users (teacher/admin).
- Attendance summaries and analytics.
- Batch promotion workflow for yearly transitions.
- Offline sync for low-connectivity classrooms.
