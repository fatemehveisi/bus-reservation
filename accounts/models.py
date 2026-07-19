from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class User(AbstractUser):
    phone_number=models.CharField(max_length=11,unique=True,verbose_name="شماره موبایل")
    national_code=models.CharField(max_length=10,unique=True,blank=True,null=True,verbose_name="کد ملی")
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"
    
#--------------------------------------------------------------------------
class Wallet(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="wallet",)
    balance=models.PositiveBigIntegerField(default=12000000)
    def __str__(self):
        return f"{self.user} - {self.balance}" 
    

