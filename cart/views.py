from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

class AddToCartView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        listing_id = request.data.get('listing')
        if not listing_id:
            return Response({'error': 'Listing ID required'}, status=400)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, listing_id=listing_id)
        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=201)

class RemoveFromCartView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        listing_id = request.data.get('listing')
        cart = Cart.objects.get(user=request.user)
        try:
            item = CartItem.objects.get(cart=cart, listing_id=listing_id)
            item.delete()
            return Response({'message': 'Removed'}, status=204)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=404)

