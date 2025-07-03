from django.contrib import admin
from .models import Inquiry

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('listing', 'name', 'email', 'created_at')
    search_fields = ('name', 'email', 'listing__title')
