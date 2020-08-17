from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from .models import *
from pprint import pprint
from django.contrib.auth.models import User
from django.db import IntegrityError
import json


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login']


class EmployerSerializer(serializers.ModelSerializer):
    user_profile = UserSerializer(read_only=True, source='user')
    user_id = serializers.IntegerField()

    class Meta:
        model = Employer
        fields = ['id', 'user_id',  'birth_date', 'phone_no', 'profile_pic', 'favorite_doers', 'user_profile']
        extra_kwargs = {'user_id': {'write_only': True}}

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        user = User.objects.filter(id=user_id).first()
        return Employer.objects.create(user=user, **validated_data)

    def validate_user_id(self, value):
        if Employer.objects.filter(user_id=value) or Doer.objects.filter(user_id=value):
            raise serializers.ValidationError('User is already taken.')
        elif not isinstance(value, int) or not User.objects.filter(id=value):
            raise serializers.ValidationError("Invalid user's id.")
        else:
            return value

    def update(self, instance, validated_data):
        req_user = self.context['request'].user

        if not req_user.is_authenticated() or req_user != Employer.objects.filter(user=req_user).first():
            pass

        instance.user_profile.username = validated_data.get('username', instance.user_profile.username)
        instance.user_profile.first_name = validated_data.get('first_name', instance.user_profile.first_name)
        instance.user_profile.last_name = validated_data.get('last_name', instance.user_profile.first_name)
        instance.user_profile.email = validated_data.get('email', instance.user_profile.first_name)
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.favorite_doers = validated_data.get('favorite_doers', instance.favorite_doers)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)



class DoerSerializer(serializers.ModelSerializer):
    user_profile = UserSerializer(read_only=True, source='user')
    user_rating = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(write_only=True)

    #TODO: FIX WRITE ONLY USER_ID IN EMPLOYER AND HERE TOO
    class Meta:
        model = Doer
        fields = ['id', 'user_id',  'user_profile', 'birth_date', 'phone_no', 'profile_pic', 'average_mark', 'professions', 'availability', 'user_rating']
        extra_kwargs = {'user_id': {'write_only': True}}
        
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        user = User.objects.filter(id=user_id).first()
        return Doer.objects.create(user=user, **validated_data)

    def validate_user_id(self, value):
 #       if Employer.objects.filter(user_id=value) or Doer.objects.filter(user_id=value):
  #          raise serializers.ValidationError('User is already taken.')
        if not isinstance(value, int) or not User.objects.filter(id=value):
            raise serializers.ValidationError("Invalid user's id.")
        else:
            return value

    def get_user_rating(self, obj):
        if request_user := self.context.get('request', None):
            request_user = self.context['request'].user
        else:
            return

        if request_user.is_authenticated and (rating := Rating.objects.filter(rater=request_user, ratee=obj.user).first()):
            return rating.rate

    def update(self, instance, validated_data):
        req_user = self.context['request'].user

        if not req_user.is_authenticated or req_user != Doer.objects.filter(user=req_user).first():
            pass

        instance.user.username = validated_data.get('username', instance.user.username)
        instance.user.first_name = validated_data.get('first_name', instance.user.first_name)
        instance.user.last_name = validated_data.get('last_name', instance.user.first_name)
        instance.user.email = validated_data.get('email', instance.user.first_name)
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        # TODO: Fix average algorithm omg
#        instance.average_mark = (instance.average_mark + validated_data.get('average_mark', instance.average_mark)) / 2
        instance.professions.set(validated_data.get('professions', instance.professions))
        instance.availability = validated_data.get('availability', instance.availability)
#       instance.user_rating = validated_data.get('user_rating', instance.user_rating)
        return instance


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
        fields = ['receiver', 'timestamp', 'message', 'read']

    def create(self, validated_data):
        request_user = self.context['request'].user

        if User.objects.filter(id=request_user.id).first():
            return Message.objects.create(sender=request_user, **validated_data)


class RequestSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'


class PersonalRequestsSerializer(serializers.ModelSerializer):
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

