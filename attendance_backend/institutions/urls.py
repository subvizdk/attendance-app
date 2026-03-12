from django.urls import path
from .views import BranchListView, LevelListView, BatchListView

urlpatterns = [
    path("branches/", BranchListView.as_view()),
    path("levels/", LevelListView.as_view()),
    path("batches/", BatchListView.as_view()),
]
