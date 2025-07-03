import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer
from listings.models import Listing

class InitiatePaymentView(APIView):
    def post(self, request):
        user = request.user
        listing_id = request.data.get('listing_id')
        amount = request.data.get('amount')

        try:
            listing = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            return Response({'error': 'Listing not found'}, status=404)

        reference = str(uuid.uuid4())

        payment = Payment.objects.create(
            user=user,
            listing=listing,
            amount=amount,
            reference=reference,
            status='pending'
        )

        # Simulate payment link (for real, you'd integrate Paystack, Flutterwave, Stripe, etc.)
        return Response({
            'message': 'Payment initialized',
            'payment_reference': reference,
            'amount': amount,
            'listing': listing.title,
            'payment_url': f"https://yourpaymentgateway.com/pay/{reference}"
        })

class ConfirmPaymentView(APIView):
    def post(self, request):
        reference = request.data.get('reference')

        try:
            payment = Payment.objects.get(reference=reference)
        except Payment.DoesNotExist:
            return Response({'error': 'Invalid payment reference'}, status=404)

        # Simulate successful confirmation
        payment.status = 'completed'
        payment.save()

        # Publish the listing
        listing = payment.listing
        listing.is_published = True
        listing.save()

        return Response({'message': 'Payment confirmed and listing published'})