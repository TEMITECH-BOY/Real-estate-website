from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'amount', 'status', 'reference', 'created_at')
    search_fields = ('user_username', 'listing_title','reference')