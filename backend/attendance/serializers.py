from rest_framework import serializers

from .models import AttendanceRecord, Batch, Student


class BatchSerializer(serializers.ModelSerializer):
    level = serializers.StringRelatedField()

    class Meta:
        model = Batch
        fields = ['id', 'name', 'academic_year', 'level', 'is_active']


class StudentSerializer(serializers.ModelSerializer):
    current_batch = BatchSerializer(read_only=True)

    class Meta:
        model = Student
        fields = [
            'id',
            'admission_number',
            'first_name',
            'last_name',
            'is_active',
            'current_batch',
        ]


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), source='student', write_only=True)

    class Meta:
        model = AttendanceRecord
        fields = ['id', 'student', 'student_id', 'date', 'status', 'remarks', 'created_at']
        read_only_fields = ['id', 'created_at', 'student']
