from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import Profile
from .models import Batch, StudentEnrollment, TeacherAssignment
from .serializers import BatchSerializer, StudentSerializer


class MyBatches(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = user.profile.role
        branch = user.profile.branch

        qs = Batch.objects.all()

        # Non-super admins are locked to their branch
        if role != Profile.ROLE_SUPER_ADMIN:
            if not branch:
                return Response([], status=200)
            qs = qs.filter(branch=branch)

        # Teachers see only batches they are assigned to
        if role == Profile.ROLE_TEACHER:
            batch_ids = TeacherAssignment.objects.filter(teacher=user).values_list("batch_id", flat=True)
            qs = qs.filter(id__in=batch_ids)

        qs = qs.select_related("course", "branch").order_by("course__name", "label")
        return Response(BatchSerializer(qs, many=True).data)


class BatchStudents(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, batch_id):
        # Optional: enforce teacher assignment check
        role = request.user.profile.role
        if role == Profile.ROLE_TEACHER:
            allowed = Batch.objects.filter(id=batch_id, teacher_assignments__teacher=request.user).exists()
            if not allowed:
                return Response({"detail": "Not allowed for this batch."}, status=403)

        enrollments = (
            StudentEnrollment.objects
            .filter(batch_id=batch_id, end_date__isnull=True)
            .select_related("student")
            .order_by("student__full_name")
        )
        students = [e.student for e in enrollments]
        return Response(StudentSerializer(students, many=True).data)
