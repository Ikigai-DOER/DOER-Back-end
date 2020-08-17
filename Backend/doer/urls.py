from rest_framework import routers
from django.conf.urls import url
from django.urls import path, include
from .views import *

# insert custom urls here
router = routers.DefaultRouter()

router.register('employer', EmployerViewSet)
router.register('doer', DoerViewSet)
router.register('request', RequestViewSet)
router.register('message', MessageViewSet)
router.register('profession', ProfessionViewSet)
router.register('report-request', ReportRequestViewSet)
router.register('report-profile', ReportProfileViewSet)
router.register('request-submission', RequestSubmissionViewSet)
router.register('personal-requests', PersonalRequestsViewSet, basename='personal-requests'),
router.register('request-search', RequestSearchViewSet, basename='request-search')

urlpatterns = [
    path('', include(router.urls)),
    path('rate-doer/', RateDoerView),
    path('user-info/', UserInfoView),
    url(r'^profile-pictures/(?P<picture_name>[\w.]{0,256})$', ProfilePicturesView)
]


