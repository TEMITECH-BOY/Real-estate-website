from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    
    # Default local image (stored in MEDIA/profile/default.jpg)
    image = models.ImageField(
        upload_to='profile',
        null=True,
        blank=True,
        default='profile/default.jpg'
    )

    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.fullname
