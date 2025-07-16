from django.urls import path
from .views import PaystackCheckoutView, PaystackVerifyView

urlpatterns = [
    path('checkout/', PaystackCheckoutView.as_view(), name='paystack-checkout'),
    path('verify/', PaystackVerifyView.as_view(), name='paystack-verify'),
]
