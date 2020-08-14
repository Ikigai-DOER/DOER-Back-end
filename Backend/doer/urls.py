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
router.register(r'report-request', ReportRequestViewSet)
router.register(r'report-profile', ReportProfileViewSet)
router.register(r'request-submission', RequestSubmissionViewSet)
router.register(r'personal-requests', PersonalRequestsViewSet, basename='personal-requests')
router.register(r'request-search', RequestSearchViewSet, basename='request-search')

urlpatterns = [
    path('', include(router.urls)),
]

