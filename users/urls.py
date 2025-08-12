from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView,
    UserDashboardView, ProfileDetailView, UpdateProfileView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileDetailView.as_view(), name='user-profile'),
    path('updateprofile/', UpdateProfileView.as_view(), name='update_profile'),
]
