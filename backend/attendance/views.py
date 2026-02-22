from rest_framework import filters, permissions, viewsets

from .models import AttendanceRecord, Batch, Student
from .serializers import AttendanceRecordSerializer, BatchSerializer, StudentSerializer


class BatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Batch.objects.filter(is_active=True).select_related('level', 'level__branch')
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'level__name', 'level__branch__name']


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.filter(is_active=True).select_related('current_batch', 'current_batch__level', 'current_batch__level__branch')
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['admission_number', 'first_name', 'last_name']


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.select_related('student', 'student__current_batch')
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date', 'created_at']
