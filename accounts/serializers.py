from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.db import transaction
from student.models import StudentModel
from Tutor.models import EmployeeModel

User = get_user_model()

class TutorRegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    address = serializers.CharField(allow_blank=True, required=False)
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    @transaction.atomic
    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        name = validated_data['name']
        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        tutor = EmployeeModel.objects.create(user=user, emp_name=name, emp_dept='', emp_id=0)
        return user


class StudentRegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    address = serializers.CharField(allow_blank=True, required=False)
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    @transaction.atomic
    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        name = validated_data['name']
        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        student = StudentModel.objects.create(user=user, name=name, roll_number=0, dept_id='')
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        attrs['user'] = user
        return attrs
