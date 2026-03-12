from rest_framework import serializers
from .models import Branch, Level, Batch

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id", "name", "code"]

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ["id", "name", "order"]

class BatchSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source="branch.name", read_only=True)
    level_name = serializers.CharField(source="level.name", read_only=True)

    class Meta:
        model = Batch
        fields = ["id", "branch", "branch_name", "level", "level_name", "name", "year", "is_active"]
