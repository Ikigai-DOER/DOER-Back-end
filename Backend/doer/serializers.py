from rest_framework import serializers
from .models import *
from pprint import pprint
from django.contrib.auth.models import User
import json


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'


class DoerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doer
        fields = ['user', 'phone_no', 'profile_pic', 'average_mark', 'professions', 'availability', 'user_rating']

    user_rating = serializers.SerializerMethodField()

    def get_user_rating(self, obj):
        request_user = self.context['request'].user

        if rating := Rating.objects.filter(rater=request_user, ratee=obj.user).first():
            return rating.rate


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = '__all__'


# TODO: create function request user (EMPLOYER ONLY)
class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'


class RequestSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestSubmission
        fields = '__all__'

    def create(self, validated_data):
        request_user = self.context['request'].user

        if doer := Doer.objects.filter(user=request_user).first():
            return RequestSubmission.objects.create(doer=doer, **validated_data)



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
        fields = ['receiver', 'timestamp', 'message']

    def create(self, validated_data):
        request_user = self.context['request'].user

        if User.objects.filter(id=request_user.id).first():
            return Message.objects.create(sender=request_user, **validated_date)


