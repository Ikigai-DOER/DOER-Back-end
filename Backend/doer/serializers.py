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
        fields = ['username', 'first_name', 'last_name', 'phone_no', 'profile_pic', 'average_mark', 'professions', 'availability', 'user_rating']

    user_rating = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    def get_user_rating(self, obj):
        request_user = self.context['request'].user

        if request_user.is_authenticated and (rating := Rating.objects.filter(rater=request_user, ratee=obj.user).first()):
            return rating.rate

    def get_username(self, obj):
        return User.objects.filter(id=obj.user.id).first().username

    def get_first_name(self, obj):
        return User.objects.filter(id=obj.user.id).first().first_name

    def get_last_name(self, obj):
        return User.objects.filter(id=obj.user.id).first().last_name


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['title', 'description', 'professions', 'doer', 'publication_date', 'expiration_date', 'location', 'price', 'status']

    def create(self, validated_data):
        request_user = self.context['request'].user

        if employer := Employer.objects.filter(user=request_user).first():
            return Request.objects.create(employer=employer, **validated_data)


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


