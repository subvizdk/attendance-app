from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = getattr(user, "profile", None)
        branch = getattr(profile, "branch", None)

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": getattr(profile, "role", None),
            "branch": {
                "id": str(branch.id),
                "city_name": branch.city_name,
            } if branch else None,
        })
