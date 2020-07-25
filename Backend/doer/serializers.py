from rest_framework import serializers
from .models import *


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'


class DoerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doer
        fields = '__all__'


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'


class RequestSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestSubmission
        fields = '__all__'


class ReportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportRequest
        fields = '__all__'


class ReportProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportProfile
        fields = '__all__'


class MessageSerializer():
    class Meta:
        model = Message
        fields = '__all__'
