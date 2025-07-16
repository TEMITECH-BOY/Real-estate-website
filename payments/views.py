import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from payments.models import Payment

class PaystackCheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = user.cart
        total_amount = int(cart.total_price() * 100)  # Paystack uses kobo

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "email": user.email,
            "amount": total_amount,
            "callback_url": "http://127.0.0.1:8000/api/payments/verify/",
        }

        response = requests.post(
            "https://api.paystack.co/transaction/initialize",
            json=data,
            headers=headers,
        )

        res_data = response.json()
        if res_data.get("status"):
            payment = Payment.objects.create(
                user=user, amount=total_amount, reference=res_data["data"]["reference"]
            )
            return Response({"authorization_url": res_data["data"]["authorization_url"]})
        else:
            return Response({"error": res_data.get("message", "Payment failed")}, status=400)


class PaystackVerifyView(APIView):
    def get(self, request):
        ref = request.GET.get('reference')
        headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        verify_response = requests.get(f"https://api.paystack.co/transaction/verify/{ref}", headers=headers)
        result = verify_response.json()

        if result.get("status") and result["data"]["status"] == "success":
            # Payment succeeded: you might mark the order as paid
            payment = Payment.objects.filter(reference=ref).first()
            if payment:
                payment.status = 'success'
                payment.save()
            return redirect("http://localhost:3000/success")  # your frontend success page
        else:
            return redirect("http://localhost:3000/cancel")
