from rest_framework import serializers
from .models import Inquiry

class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'response', 'answered', 'user']
        extra_kwargs = {
            'email': {'required': True},
            'name': {'required': True},
            'message': {'required': True},
            'listing': {'required': True}
        }
