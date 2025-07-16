# users/urls.py
from django.urls import path
from . import views
from .views import ProfileDetailView

urlpatterns = [
    path('register/',views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),
     path('profile/', ProfileDetailView.as_view(), name='user-profile'),
    path('updateprofile/', views.updateProfileView.as_view(), name='update_profile'),

    
]