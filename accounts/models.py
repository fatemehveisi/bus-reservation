from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number=models.CharField(max_length=11,unique=True,null=True)
    national_code=models.CharField(max_length=10,unique=True,blank=True,null=True)
    def __str__(self):
        return self.username

