from django.db import models
from django.conf import settings
from listings.models import Listing  # adjust to your actual Listing model import

class Inquiry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='inquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    response = models.TextField(blank=True, null=True)  # optional: store admin response
    answered = models.BooleanField(default=False)      # optional: mark as answered

    def __str__(self):
        return f"Inquiry by {self.name} on {self.listing}"

