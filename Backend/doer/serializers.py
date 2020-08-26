from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from .models import *
from pprint import pprint
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
import json


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login']
        extra_kwargs = {
            'username': {'validators': []},
        }


class EmployerSerializer(serializers.ModelSerializer):
    user_profile = UserSerializer(source='user')
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Employer
        fields = ['id', 'user_id', 'birth_date', 'phone_no', 'profile_pic', 'favorite_doers', 'user_profile']

    def create(self, validated_data):
        validated_data.pop('user')
        user_id = validated_data.pop('user_id')
        user = User.objects.filter(id=user_id).first()
        return Employer.objects.create(user=user, **validated_data)

    def validate_user_id(self, value):
        #       if Employer.objects.filter(user_id=value) or Doer.objects.filter(user_id=value):
        #          raise serializers.ValidationError('User is already taken.')
        if not isinstance(value, int) or not User.objects.filter(id=value):
            raise serializers.ValidationError("Invalid user's id.")
        else:
            return value

    def update(self, instance, validated_data):
        req_user = self.context['request'].user

        if not Employer.objects.filter(user=req_user):
            raise serializers.ValidationError('Not authenticated or user taken.')
        user_serializer = self.fields['user_profile']
        user_instance = instance.user
        user_data = validated_data.get('user', None)
        if user_data and user_instance:
            user_serializer.update(user_instance, user_data)
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        # TODO: Fix this
        instance.favorite_doers.clear()
        for doer in validated_data.get('favorite_doers', instance.favorite_doers):
            instance.favorite_doers.add(doer)
        instance.save()

        return instance


class DoerSerializer(serializers.ModelSerializer):
    user_profile = UserSerializer(source='user')
    user_rating = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Doer
        fields = ['id', 'user_id', 'user_profile', 'birth_date', 'phone_no', 'profile_pic', 'average_mark',
                  'professions', 'availability', 'user_rating']
        read_only_fields = ('average_mark', 'user_rating')

    def create(self, validated_data):
        validated_data.pop('user')
        user_id = validated_data.pop('user_id')
        user = User.objects.filter(id=user_id).first()
        return Doer.objects.create(user=user, **validated_data)

    # FIX: if update don't do the check? (doer too)
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

        if request_user.is_authenticated and (
        rating := Rating.objects.filter(rater=request_user, ratee=obj.user).first()):
            return rating.rate

    def update(self, instance, validated_data):
        req_user = self.context['request'].user

        if not Doer.objects.filter(user=req_user):
            raise serializers.ValidationError('Not authenticated or user taken.')
        user_serializer = self.fields['user_profile']
        user_instance = instance.user
        user_data = validated_data.get('user', None)
        if user_data and user_instance:
            user_serializer.update(user_instance, user_data)
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.availability = validated_data.get('availability', instance.availability)
        # should be fixed, pretty bad
        instance.professions.clear()
        professions = validated_data.get('professions', instance.professions)
        for profession in professions:
            instance.professions.add(profession)

        instance.availability = validated_data.get('availability', instance.availability)
        instance.save()

        return instance


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    employer = EmployerSerializer(read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'title', 'employer', 'description', 'professions', 'doer', 'publication_date',
                  'expiration_date', 'location', 'price', 'status']

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
        read_only_fields = ('doer',)

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
        fields = ['receiver', 'sender', 'timestamp', 'message', 'read']
        read_only_fields = ('sender')
        ordering = ['-read', 'timestamp']

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
        fields = ['username', 'email', 'first_name', 'last_name',
                  'password1', 'password2', ]
        extra_kwargs = {
            'password': {
                'write_only': True
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


class MyRequestsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'title', 'employer', 'description', 'professions', 'doer', 'publication_date',
                  'expiration_date', 'location', 'price', 'status']

