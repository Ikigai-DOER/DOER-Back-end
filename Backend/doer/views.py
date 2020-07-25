from rest_framework import viewsets
from .serializers import *
from .models import *


class EmployerViewSet(viewsets.ModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer


class DoerViewSet(viewsets.ModelViewSet):
    queryset = Doer.objects.all()
    serializer_class = DoerSerializer


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class RequestSubmissionViewSet(viewsets.ModelViewSet):
    queryset = RequestSubmission.objects.all()
    serializer_class = RequestSubmissionSerializer


class ReportRequestViewSet(viewsets.ModelViewSet):
    queryset = ReportRequest.objects.all()
    serializer_class = ReportRequestSerializer


class ReportProfileViewSet(viewsets.ModelViewSet):
    queryset = ReportProfile.objects.all()
    serializer_class = ReportProfileSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

