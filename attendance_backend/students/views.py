from rest_framework import generics
from .models import Student
from .serializers import StudentSerializer

class StudentsByBatchView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        batch_id = self.kwargs["batch_id"]
        return (
            Student.objects.filter(
                batch_assignments__batch_id=batch_id,
                batch_assignments__ended_at__isnull=True,
                is_active=True,
            )
            .distinct()
            .order_by("student_id")
        )

class StudentDetailView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
