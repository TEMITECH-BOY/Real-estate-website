from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'reference', 'amount', 'status', 'created_at']
    search_fields = ['reference', 'user__username']
    list_filter = ['status']
