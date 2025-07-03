from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Inquiry
from .serializers import InquirySerializer
from django.core.mail import send_mail


class SubmitInquiryView(APIView):
    def post(self, request):
        data = request.data.copy()
        if request.user.is_authenticated:
            data['user'] = request.user.id
        serializer = InquirySerializer(data=data)
        if serializer.is_valid():
            send_mail(
                 subject=f'New Inquiry for {serializer.validated_data["listing"]}',
                 message=serializer.validated_data["message"],
                 from_email=serializer.validated_data["email"],
                 recipient_list=['youradmin@example.com'],
                 fail_silently=False,
            )
            serializer.save()
            return Response({'message': 'Inquiry submitted successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
