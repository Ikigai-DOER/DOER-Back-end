from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import *
from .models import *


class EmployerViewSet(viewsets.ModelViewSet):
    queryset = Employer.objects.all()
    #permission_classes = [IsAuthenticated]
    serializer_class = EmployerSerializer


class DoerViewSet(viewsets.ModelViewSet):
    queryset = Doer.objects.all()
    #permission_classes = [IsAuthenticated]
    serializer_class = DoerSerializer


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProfessionSerializer


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    #permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer


class RequestSubmissionViewSet(viewsets.ModelViewSet):
    queryset = RequestSubmission.objects.all()
    #permission_classes = [IsAuthenticated]
    serializer_class = RequestSubmissionSerializer


class ReportRequestViewSet(viewsets.ModelViewSet):
    queryset = ReportRequest.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ReportRequestSerializer


class ReportProfileViewSet(viewsets.ModelViewSet):
    queryset = ReportProfile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ReportProfileSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer


class RequestSearchViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        filter_professions = request.GET.get('professions', []).split(',')
        queryset = Request.objects.all().filter(professions__in=filter_professions)
        serializer = RequestSearchSerializer(queryset, many=True)
        return Response(serializer.data)


