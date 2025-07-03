from django.contrib import admin
from .models import Listing
from django.utils.html import format_html

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_published', 'created_at' ,'thumbnail')
    list_filter = ('category', 'is_published', 'created_at')
    search_fields = ('title', 'description', 'location')
    list_editable = ('is_published',)
    ordering = ('-created_at',)
    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="40" />', obj.image.url)
        return "-"
    thumbnail.short_description = 'Image'

    
