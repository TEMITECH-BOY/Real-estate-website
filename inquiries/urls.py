from django.urls import path
from .views import SubmitInquiryView, SendResponseView

urlpatterns = [
    path('submit/', SubmitInquiryView.as_view(), name='submit-inquiry'),
    path('response/<int:inquiry_id>/respond/', SendResponseView.as_view(), name='send-response'),
]
