from rest_framework import routers
from django.urls import path, include
from .views import *

# insert custom urls here
router = routers.DefaultRouter()

router.register(r'employer', EmployerViewSet)
router.register(r'doer', DoerViewSet)
router.register(r'request', RequestViewSet)
router.register(r'message', MessageViewSet)
router.register(r'profession', ProfessionViewSet)
router.register(r'request-submission', RequestSubmissionViewSet)
router.register(r'report-request', ReportRequestViewSet)
router.register(r'report-profile', ReportProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

