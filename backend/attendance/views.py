from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import AttendanceSession, AttendanceRecord
from academics.models import StudentEnrollment

class CreateOrGetSession(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        batch_id = request.data.get("batch_id")
        date = request.data.get("date")  # YYYY-MM-DD

        if not batch_id or not date:
            return Response({"detail": "batch_id and date required"}, status=400)

        branch = request.user.profile.default_branch
        if not branch:
            return Response({"detail": "User has no default branch"}, status=400)

        session, _ = AttendanceSession.objects.get_or_create(
            batch_id=batch_id,
            date=date,
            defaults={"branch": branch, "taken_by": request.user},
        )

        return Response({"session_id": session.id, "status": session.status})

class SessionSheet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        session = AttendanceSession.objects.get(id=session_id)

        enrollments = StudentEnrollment.objects.filter(batch=session.batch, end_date__isnull=True).select_related("student")
        students = [e.student for e in enrollments]

        existing = AttendanceRecord.objects.filter(session=session)
        m = {r.student_id: r for r in existing}

        rows = []
        for s in students:
            r = m.get(s.id)
            rows.append({
                "student_id": s.id,
                "student_name": s.full_name,
                "admission_no": s.admission_no,
                "status": r.status if r else "PRESENT",
                "note": r.note if r else "",
            })

        return Response({"session_id": session.id, "date": str(session.date), "batch_id": session.batch_id, "students": rows})

class BulkSaveAttendance(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def put(self, request, session_id):
        session = AttendanceSession.objects.get(id=session_id)
        if session.status == "LOCKED":
            return Response({"detail": "Session locked"}, status=400)

        items = request.data.get("items", [])
        for it in items:
            AttendanceRecord.objects.update_or_create(
                session=session,
                student_id=it["student_id"],
                defaults={
                    "status": it.get("status", "PRESENT"),
                    "note": it.get("note", ""),
                }
            )
        return Response({"detail": "Saved"})

class SubmitAttendance(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        session = AttendanceSession.objects.get(id=session_id)
        session.status = "SUBMITTED"
        session.save()
        return Response({"detail": "Submitted"})