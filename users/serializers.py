from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from .utils import sendMail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# ------------------------------
# ✅ Register Serializer
# ------------------------------
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    fullname = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    image = serializers.ImageField(required=False)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match"})

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username already taken"})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email already registered"})

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        user = User.objects.create_user(username=username, email=email, password=password)

        # Create profile with remaining fields
        Profile.objects.create(user=user, **validated_data)

        sendMail(email, validated_data.get('fullname', ''))
        return user

# ------------------------------
# ✅ Profile Serializer
# ------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'fullname', 'gender', 'phone', 'image']

# ------------------------------
# ✅ Update User/Profile Serializer
# ------------------------------
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

# ------------------------------
# ✅ Custom Token Serializer
# ------------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['email'] = self.user.email
        return data
