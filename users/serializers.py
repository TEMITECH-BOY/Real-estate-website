from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
from .utils import sendMail


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'fullname', 'gender', 'phone', 'image']


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['fullname', 'username', 'email', 'password', 'confirm_password', 'gender', 'phone', 'image']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        
         # Check if username already exists
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already taken")

        # Check if email already exists
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already registered")

        return data

    def create(self, validated_data):
        # Extract user fields
       username = validated_data.pop('username')
       email = validated_data.pop('email')
       password = validated_data.pop('password')
       validated_data.pop('confirm_password')  # Remove confirm_password

       # Create user
       user = User.objects.create_user(username=username, email=email, password=password)

       # Create profile
       profile = Profile.objects.create(user=user, **validated_data)

       # Send mail with email and fullname
       sendMail(email, validated_data.get('fullname'))

       return profile


# Update User/Profile Serializer
class UpdateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.EmailField(source='user.email', required=False)

    class Meta:
        model = Profile
        fields = ['fullname', 'username', 'email', 'gender', 'phone', 'image']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        if 'username' in user_data:
            user.username = user_data['username']
        if 'email' in user_data:
            user.email = user_data['email']
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
