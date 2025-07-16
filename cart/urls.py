from django.urls import path
from .views import CartView, AddToCartView, RemoveFromCartView

urlpatterns = [
    path('', CartView.as_view(), name='user-cart'),
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove/', RemoveFromCartView.as_view(), name='remove-from-cart'),
]
