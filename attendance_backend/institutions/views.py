from rest_framework import generics
from .models import Branch, Level, Batch
from .serializers import BranchSerializer, LevelSerializer, BatchSerializer

class BranchListView(generics.ListAPIView):
    queryset = Branch.objects.all().order_by("name")
    serializer_class = BranchSerializer

class LevelListView(generics.ListAPIView):
    queryset = Level.objects.all().order_by("order", "name")
    serializer_class = LevelSerializer

class BatchListView(generics.ListAPIView):
    serializer_class = BatchSerializer

    def get_queryset(self):
        qs = Batch.objects.select_related("branch", "level").all()
        branch_id = self.request.query_params.get("branch_id")
        level_id = self.request.query_params.get("level_id")
        year = self.request.query_params.get("year")
        is_active = self.request.query_params.get("is_active")

        if branch_id:
            qs = qs.filter(branch_id=branch_id)
        if level_id:
            qs = qs.filter(level_id=level_id)
        if year:
            qs = qs.filter(year=year)
        if is_active in ("true", "false"):
            qs = qs.filter(is_active=(is_active == "true"))

        return qs.order_by("-year", "name")
