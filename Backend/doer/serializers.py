from rest_framework import serializers
from .models import *
from pprint import pprint
from django.contrib.auth.models import User
import json


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login']


class EmployerSerializer(serializers.ModelSerializer):
    user_profile = UserSerializer(read_only=True, source='user')

    class Meta:
        model = Employer
        fields = ['phone_no', 'profile_pic', 'favorite_doers', 'user_profile']


class DoerSerializer(serializers.ModelSerializer):
    user_profile = UserSerializer(read_only=True, source='user')

    class Meta:
        model = Doer
        fields = ['user_profile', 'phone_no', 'profile_pic', 'average_mark', 'professions', 'availability', 'user_rating']

    user_rating = serializers.SerializerMethodField()

    def get_user_rating(self, obj):
        request_user = self.context['request'].user

        if request_user.is_authenticated and (rating := Rating.objects.filter(rater=request_user, ratee=obj.user).first()):
            return rating.rate


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    employer = EmployerSerializer(read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'title', 'employer', 'description', 'professions', 'doer', 'publication_date', 'expiration_date', 'location', 'price', 'status']

    def create(self, validated_data):
        request_user = self.context['request'].user

        if employer := Employer.objects.filter(user=request_user).first():
            professions = validated_data.pop('professions')
            request = Request.objects.create(employer=employer, **validated_data)
            request.professions.add(*professions)
            return request


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


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['receiver', 'timestamp', 'message']

    def create(self, validated_data):
        request_user = self.context['request'].user

        if User.objects.filter(id=request_user.id).first():
            return Message.objects.create(sender=request_user, **validated_date)


class RequestSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'
