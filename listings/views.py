from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import Listing
from .serializers import ListingSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ListingFilter

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ListingFilter


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user




class ListingViewSet(viewsets.ModelViewSet):
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description', 'category']
    filterset_fields = ['category', 'is_available', 'price']  # Add fields you want to filter

    def get_queryset(self):
        return Listing.objects.filter(is_published=True, is_available=True)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ListingDetailViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Listing.objects.filter(is_published=True, is_available=True)



