from django.urls import path
from .views import CreateOrGetSession, SessionSheet, BulkSaveAttendance, SubmitAttendance

urlpatterns = [
    path("sessions/", CreateOrGetSession.as_view()),
    path("sessions/<int:session_id>/", SessionSheet.as_view()),
    path("sessions/<int:session_id>/bulk/", BulkSaveAttendance.as_view()),
    path("sessions/<int:session_id>/submit/", SubmitAttendance.as_view()),
]
