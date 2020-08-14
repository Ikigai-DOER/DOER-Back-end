from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from .models import *
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


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
        if rating_obj := Rating.objects.filter(rater=request.rater, ratee=doer.user):
            rating_obj.rate = rate
            try:
                doer.average_mark = doer.average_mark * doer.number_rates - (doer.average_mark - float(rate))
            except TypeError:
                return HttpResponse(status=400)
        else:
            Rating.objects.create(rater=request.user, ratee=doer.user, rate=rate).save()
            doer.number_rates += 1
            try:
                doer.average_mark = (doer.average_mark + float(rate)) / doer.number_rates
            except TypeError:
                return HttpResponse(status=400)

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
            return Request.objects.filter(doer=doer.first())
        elif employer := Employer.objects.filter(user=self.request.user):
            return Request.objects.filter(employer=employer.first())


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


class RequestSearchViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        filter_professions = request.GET.get('professions', []).split(',')
        print(filter_professions)
        queryset = Request.objects.all().filter(professions__in=filter_professions)
        serializer = RequestSearchSerializer(queryset, many=True)
        return Response(serializer.data)

