from django.urls import path
from .views import ExamsByBatch, MarksSheet

urlpatterns = [
    path("", ExamsByBatch.as_view()),                  # /api/exams?batch_id=1
    path("<int:exam_id>/marks/", MarksSheet.as_view()),# /api/exams/1/marks/
]
