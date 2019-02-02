from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from PIL import Image

# Create your models here.



class CustomUser(AbstractUser):
    verified = models.BooleanField(verbose_name='verified', default=False)
    primary = models.BooleanField(verbose_name='primary', default=False)
    def __str__(self):
        return self.email



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=300, blank=True)
    image = models.ImageField(default="default.png", upload_to='profile_pics')


    def __str__(self):
        return f'{self.user.username}Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
