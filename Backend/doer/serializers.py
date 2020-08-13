from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import *
from pprint import pprint
from django.contrib.auth.models import User
import json


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login']


class EmployerSerializer(serializers.ModelSerializer):
    user_profile = UserSerializer(source='user')

    class Meta:
        model = Employer
        fields = ['birth_date', 'phone_no', 'profile_pic', 'favorite_doers', 'user_profile']

#    def create(self, validated_data):
#            userProfile = validated_data.pop('user')
#            user = User.objects.create(**userProfile)
#            return Employer.objects.create(user=user, **validated_data)
            
            
class DoerSerializer(serializers.ModelSerializer):
    user_profile = UserSerializer(source='user')
    user_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Doer
        fields = ['user_profile', 'birth_date', 'phone_no', 'profile_pic', 'average_mark', 'professions', 'availability', 'user_rating']
        
#    def create(self, validated_data):
#        userProfile = validated_data.pop('user')
#        user = User.objects.create(**userProfile)
#        return Doer.objects.create(user=user, **validated_data)

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
        fields = ['title', 'employer', 'description', 'professions', 'doer', 'publication_date', 'expiration_date', 'location', 'price', 'status']

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


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['receiver', 'timestamp', 'message', 'read']

    def create(self, validated_data):
        request_user = self.context['request'].user

        if User.objects.filter(id=request_user.id).first():
            return Message.objects.create(sender=request_user, **validated_data)


class RequestSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'



class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name','last_name',
        'password1', 'password2',]
        extra_kwargs = {
            'password': {
                'write_only':True
            }
        }

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
        }

