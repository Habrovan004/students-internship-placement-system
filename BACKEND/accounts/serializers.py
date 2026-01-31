from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StudentProfile, CompanyProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all(), write_only=True)

    class Meta:
        model = StudentProfile
        fields = ("id", "user", "user_id", "programme", "year_of_study")


class CompanyProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all(), write_only=True)

    class Meta:
        model = CompanyProfile
        fields = ("id", "user", "user_id", "company_name", "location", "discription")