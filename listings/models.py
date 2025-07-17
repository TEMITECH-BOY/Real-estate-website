from django.db import models
from django.db import models
from users.models import User

class Listing(models.Model):
    CATEGORY_CHOICES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    image = models.ImageField(upload_to='listing_images/')
    is_published = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


