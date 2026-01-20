from django.urls import path
from .views import MyBatches, BatchStudents

urlpatterns = [
    path("my-batches/", MyBatches.as_view(), name="my-batches"),
    path("batches/<int:batch_id>/students/", BatchStudents.as_view(), name="batch-students"),
]
