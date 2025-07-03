from django.db import models
from django.contrib.auth.models import User


GENDER_CHOICES=(
    ('M''Male'),
    ('F''Female'),
)

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=6,choices=GENDER_CHOICES)
    image = models.ImageField(upload_to='profile', null=True, blank=True, default="https://media.istockphoto.com/id/1459664492/vector/default-avatar-profile-user-profile-icon-profile-picture-portrait-symbol-user-member-people.jpg?s=612x612&w=0&k=20&c=NxWFtww0PspmB8u-wjHkxOyeS8aviOr9UIWTchgG8LU=")
    created =models.DateField(auto_now_add=True)
    def _str_(self):
      return self.fullname