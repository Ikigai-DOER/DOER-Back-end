from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from rest_framework import viewsets
from django.core import serializers as core_serializers
from django.http import JsonResponse
from .serializers import *
from .models import *
from django.conf import settings
from django.shortcuts import render
from django.db.models import Q
import os
import magic

@csrf_exempt
def AccountConfirmView(request, token):
    return render(request, 'doer/verification.html', {'token': token})

@csrf_exempt
@api_view(['GET'])
def ProfilePicturesView(request, picture_name):
    try:
        print(settings.MEDIA_ROOT)
        path_to_pic = os.path.join(settings.MEDIA_ROOT, picture_name)
        print(path_to_pic)
        with open(path_to_pic, "rb") as f:
            mime_type = magic.from_file(path_to_pic, mime=True)
            return HttpResponse(f.read(), content_type=mime_type)
    except IOError:
        return HttpResponse(status=303)


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserInfoView(request):
    user_id = request.GET.get('userId', None)
    
    if not user_id:
        return HttpResponse(status=400)

    if doer := Doer.objects.filter(user_id=user_id):
        return JsonResponse({'user': DoerSerializer(doer.first()).data, 'doer': True})

    if employer := Employer.objects.filter(user_id=user_id):
        return JsonResponse({'user': EmployerSerializer(employer.first()).data, 'doer': False})

    return HttpResponse(status=404)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def RateDoerView(request):
    rate = request.GET.get('rate', None)
    ratee = request.GET.get('ratee', None)

    if rate is None or ratee is None:
        return HttpResponse(status=400)

    if doer := Doer.objects.filter(id=ratee):
        doer = doer.first()
        if rating_obj := Rating.objects.filter(rater=request.user, ratee=doer.user):
            rating_obj.rate = rate
            doer.average_mark = float(doer.average_mark) * doer.number_rates - (float(doer.average_mark) - float(rate))
        else:
            rating_obj = Rating.objects.create(rater=request.user, ratee=doer.user, rate=rate)
            doer.number_rates += 1
 #           try:
            doer.average_mark = ((float(doer.average_mark) or 0) + float(rate)) / float(doer.number_rates)

        rating_obj.save()
        doer.save()
        return HttpResponse(status=200)

    return HttpResponse(status=400)


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
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer


class PersonalRequestsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PersonalRequestsSerializer

    def get_queryset(self):
        if doer := Doer.objects.filter(user=self.request.user):
            return self.queryset.filter(doer=doer.first())
        elif employer := Employer.objects.filter(user=self.request.user):
            return self.queryset.filter(employer=employer.first())


class RequestSubmissionViewSet(viewsets.ModelViewSet):
    queryset = RequestSubmission.objects.all()
    permission_classes = [IsAuthenticated]
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

    def get_queryset(self):
        req_user = self.request.user
        return self.queryset.filter(Q(sender=req_user) | Q(receiver=req_user))

class RequestSearchViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        filter_professions = request.GET.get('professions', []).split(',')
        queryset = Request.objects.all().filter(professions__in=filter_professions)
        serializer = RequestSearchSerializer(queryset, many=True)
        return Response(serializer.data)

