from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import AttendanceSession, AttendanceMark
from .serializers import AttendanceSessionSerializer, CreateOrGetSessionSerializer, MarksBulkSerializer

class AttendanceSessionDetailView(generics.RetrieveAPIView):
    queryset = AttendanceSession.objects.prefetch_related("marks", "marks__student").all()
    serializer_class = AttendanceSessionSerializer
    permission_classes = [IsAuthenticated]

class CreateOrGetSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        s = CreateOrGetSessionSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        obj, _ = AttendanceSession.objects.get_or_create(
            batch=s.validated_data["batch"],
            date=s.validated_data["date"],
            label=s.validated_data["label"],
        )
        return Response(AttendanceSessionSerializer(obj).data, status=status.HTTP_200_OK)

class SubmitMarksView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, session_id: int):
        payload = MarksBulkSerializer(data=request.data)
        payload.is_valid(raise_exception=True)

        session = AttendanceSession.objects.get(id=session_id)
        objs = [
            AttendanceMark(session=session, student_id=m["student"], status=m["status"])
            for m in payload.validated_data["marks"]
        ]

        with transaction.atomic():
            AttendanceMark.objects.bulk_create(
                objs,
                update_conflicts=True,
                unique_fields=["session", "student"],
                update_fields=["status", "noted_at"],
            )

        return Response({"ok": True, "count": len(objs)}, status=status.HTTP_200_OK)

class BatchAttendanceSessionsView(generics.ListAPIView):
    serializer_class = AttendanceSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        batch_id = self.kwargs["batch_id"]
        qs = AttendanceSession.objects.filter(batch_id=batch_id).prefetch_related("marks", "marks__student")
        limit = self.request.query_params.get("limit")
        if limit and limit.isdigit():
            return qs[: int(limit)]
        return qs
