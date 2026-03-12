from django.urls import path
from .views import StudentsByBatchView, StudentDetailView

urlpatterns = [
    path("batches/<int:batch_id>/students/", StudentsByBatchView.as_view()),
    path("students/<int:pk>/", StudentDetailView.as_view()),
]
