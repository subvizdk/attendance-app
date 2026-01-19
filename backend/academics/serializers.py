from rest_framework import serializers
from .models import Batch, Student


class BatchSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = Batch
        fields = ["id", "branch", "course", "course_name", "year", "label"]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "id",
            "branch",
            "admission_no",
            "full_name",
            "father_full_name",
            "mother_full_name",
            "email",
            "phone",
        ]
