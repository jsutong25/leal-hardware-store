from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=12, null=True)
    image = models.ImageField(upload_to='profile_images', default='defaultprofile.jpg')

    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} - Profile"