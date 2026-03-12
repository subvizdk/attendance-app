from rest_framework import serializers
from .models import AttendanceSession, AttendanceMark
from students.serializers import StudentSerializer

class AttendanceMarkSerializer(serializers.ModelSerializer):
    student_detail = StudentSerializer(source="student", read_only=True)

    class Meta:
        model = AttendanceMark
        fields = ["student", "status", "noted_at", "student_detail"]

class AttendanceSessionSerializer(serializers.ModelSerializer):
    marks = AttendanceMarkSerializer(many=True, read_only=True)

    class Meta:
        model = AttendanceSession
        fields = ["id", "batch", "date", "label", "created_at", "marks"]

class CreateOrGetSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceSession
        fields = ["batch", "date", "label"]

class MarkItemSerializer(serializers.Serializer):
    student = serializers.IntegerField()
    status = serializers.ChoiceField(choices=[c[0] for c in AttendanceMark.Status.choices])

class MarksBulkSerializer(serializers.Serializer):
    marks = MarkItemSerializer(many=True)
