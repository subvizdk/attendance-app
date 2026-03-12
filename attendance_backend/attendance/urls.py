from django.urls import path
from .views import CreateOrGetSessionView, SubmitMarksView, AttendanceSessionDetailView, BatchAttendanceSessionsView

urlpatterns = [
    path("attendance/sessions/", CreateOrGetSessionView.as_view()),
    path("attendance/sessions/<int:pk>/", AttendanceSessionDetailView.as_view()),
    path("attendance/sessions/<int:session_id>/marks/", SubmitMarksView.as_view()),
    path("batches/<int:batch_id>/attendance/sessions/", BatchAttendanceSessionsView.as_view()),
]
