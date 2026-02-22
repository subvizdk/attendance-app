from rest_framework.routers import DefaultRouter

from .views import AttendanceRecordViewSet, BatchViewSet, StudentViewSet

router = DefaultRouter()
router.register('batches', BatchViewSet, basename='batch')
router.register('students', StudentViewSet, basename='student')
router.register('attendance', AttendanceRecordViewSet, basename='attendance')

urlpatterns = router.urls
