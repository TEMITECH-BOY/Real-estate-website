from rest_framework import serializers
from . models import Profile
from django.contrib.auth.models import User

from . utils import sendMail


# Serializer DJango User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username', 'email', ]

# Serializer Profile
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserSerializer()
        fields = ['fullname', 'gender', 'phone', 'image']

#register serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    class Meta:
        model= Profile
        fields= ['fullname','username', 'email','password', 'confirm_password','gender', 'phone', 'image']
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    def create(self, validated_data):
        username=validated_data.pop['username'],
        email=validated_data.pop['email'],
        password=validated_data.pop['password']
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()


# update user serializer
class UpdateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    class Meta:
        model = Profile
        fields = ['fullname', 'username', 'email','gender', 'phone', 'image']
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        if 'username' in user_data:
            user.username = user_data['username']
        if 'email' in user_data:
            user.email = user_data['email']
        user.save()
        instance.fullname = validated_data.get('fullname')
        instance.gender = validated_data.get('gender')
        instance.phone = validated_data.get('phone')
        instance.image = validated_data.get('image')
        instance.save()
        return instance
 


   