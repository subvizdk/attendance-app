from rest_framework import serializers
from django.contrib.auth.models import User


class MeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="profile.role", read_only=True)
    branch_id = serializers.UUIDField(source="profile.branch.id", read_only=True, allow_null=True)
    branch_city = serializers.CharField(source="profile.branch.city_name", read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "branch_id", "branch_city"]
