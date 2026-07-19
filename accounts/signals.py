from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from .models import Wallet

user=get_user_model()

@receiver(post_save,sender=user)
def create_wallet(sender,instance,created,**kwargs):
    if created:
        Wallet.objects.get_or_create(user=instance)