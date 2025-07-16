from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Inquiry
from .serializers import InquirySerializer
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

class SubmitInquiryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id  # ensure user is set
        serializer = InquirySerializer(data=data)
        if serializer.is_valid():
            # send_mail(
            #     subject=f'New Inquiry for listing ID {serializer.validated_data["listing"]}',
            #     message=serializer.validated_data["message"],
            #     from_email=serializer.validated_data["email"],
            #     recipient_list=['temitayoosunla@gmail.com'],
            #     fail_silently=False,
            # )
            serializer.save()
            return Response({'message': 'Inquiry submitted successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendResponseView(APIView):
    def post(self, request, inquiry_id):
        try:
            inquiry = Inquiry.objects.get(id=inquiry_id)
        except Inquiry.DoesNotExist:
            return Response({'error': 'Inquiry not found'}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        response_message = request.data.get('response')
        if not response_message:
            return Response({'error': 'Response message is required'}, status=status.HTTP_400_BAD_REQUEST)

        send_mail(
            subject='Response to your inquiry',
            message=response_message,
            from_email='youradmin@example.com',
            recipient_list=[inquiry.email],  # send to the person who made the inquiry
            fail_silently=False,
        )

        # Optionally, save the response in the Inquiry object (add a field like `response` or `answered`)
        # inquiry.response = response_message
        # inquiry.answered = True
        # inquiry.save()

        return Response({'message': 'Response sent successfully'}, status=status.HTTP_200_OK)
