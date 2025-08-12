from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        listing_id = request.data.get('listing')
        if not listing_id:
            return Response({'error': 'Listing ID required'}, status=400)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, listing_id=listing_id)

        # Optionally, increase quantity instead of duplicate items
        # if not created:
        #     item.quantity += 1
        #     item.save()

        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=201 if created else 200)


class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        listing_id = request.data.get('listing')
        if not listing_id:
            return Response({'error': 'Listing ID required'}, status=400)

        try:
            cart = Cart.objects.get(user=request.user)
            item = CartItem.objects.get(cart=cart, listing_id=listing_id)
            item.delete()
            return Response({'message': 'Removed'}, status=200)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=404)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=404)


