from rest_framework.routers import DefaultRouter

from .views.driver import DriverViewSet
from .views.driver_log import DriverLogViewSet

router = DefaultRouter()
router.register('drivers', DriverViewSet, basename='drivers')
router.register('driver-logs', DriverLogViewSet, basename='driver-logs')

urlpatterns = [

]

urlpatterns += router.urls
