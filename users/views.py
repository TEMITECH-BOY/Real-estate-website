from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from .serializers import (
    RegisterSerializer,
    UpdateUserSerializer,
    ProfileSerializer,
    CustomTokenObtainPairSerializer
)



# ------------------------------
# ✅ Register view
# ------------------------------
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------
# ✅ Login view
# ------------------------------
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

# ------------------------------
# ✅ Logout
# ------------------------------
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

# ------------------------------
# ✅ Dashboard view (profile data)
# ------------------------------
class UserDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response({"message": "User dashboard retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)

# ------------------------------
# ✅ Profile details
# ------------------------------
class ProfileDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ------------------------------
# ✅ Update profile
# ------------------------------
class UpdateProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = UpdateUserSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        profile = request.user.profile
        serializer = UpdateUserSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
