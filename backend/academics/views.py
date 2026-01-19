from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import Profile
from .models import Batch, StudentEnrollment
from .serializers import BatchSerializer, StudentSerializer


class MyBatches(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = user.profile.role
        branch = user.profile.branch  # ✅ was default_branch

        qs = Batch.objects.all()

        # ✅ Role constants live on Profile now
        if role != Profile.ROLE_SUPER_ADMIN:
            if not branch:
                return Response([], status=200)
            qs = qs.filter(branch=branch)

        if role == Profile.ROLE_TEACHER:
            qs = qs.filter(teacher_assignments__teacher=user)

        return Response(BatchSerializer(qs.order_by("course__name", "label"), many=True).data)


class BatchStudents(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, batch_id):
        enrollments = (
            StudentEnrollment.objects
            .filter(batch_id=batch_id, end_date__isnull=True)
            .select_related("student")
        )
        students = [e.student for e in enrollments]
        return Response(StudentSerializer(students, many=True).data)