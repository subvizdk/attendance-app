from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import Exam, Mark
from academics.models import StudentEnrollment

class ExamsByBatch(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        batch_id = request.query_params.get("batch_id")
        if not batch_id:
            return Response({"detail": "batch_id required"}, status=400)

        qs = Exam.objects.filter(batch_id=batch_id).order_by("-date")
        data = [{"id": e.id, "title": e.title, "date": str(e.date), "max_marks": e.max_marks, "status": e.status} for e in qs]
        return Response(data)

class MarksSheet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, exam_id):
        exam = Exam.objects.get(id=exam_id)

        enrollments = StudentEnrollment.objects.filter(batch=exam.batch, end_date__isnull=True).select_related("student")
        students = [e.student for e in enrollments]

        existing = Mark.objects.filter(exam=exam)
        m = {mk.student_id: mk for mk in existing}

        rows = []
        for s in students:
            mk = m.get(s.id)
            rows.append({
                "student_id": s.id,
                "student_name": s.full_name,
                "admission_no": s.admission_no,
                "marks_obtained": mk.marks_obtained if mk else 0,
                "note": mk.note if mk else "",
            })

        return Response({
            "exam": {"id": exam.id, "title": exam.title, "date": str(exam.date), "max_marks": exam.max_marks, "status": exam.status},
            "students": rows
        })

    @transaction.atomic
    def put(self, request, exam_id):
        exam = Exam.objects.get(id=exam_id)
        items = request.data.get("items", [])
        for it in items:
            Mark.objects.update_or_create(
                exam=exam,
                student_id=it["student_id"],
                defaults={"marks_obtained": it.get("marks_obtained", 0), "note": it.get("note", "")}
            )
        return Response({"detail": "Marks saved"})