from django.db import models
from django.contrib.auth.models import User
from listings.models import Listing  # Adjust import if your app is named differently
from django.conf import settings

  


class Inquiry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Inquiry for {self.listing.title} by {self.name}"
