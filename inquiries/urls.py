from django.urls import path
from .views import SubmitInquiryView

urlpatterns = [
    path('submit/', SubmitInquiryView.as_view()),
]