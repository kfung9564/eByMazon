from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class UserApplication(models.Model):
    username = models.CharField(unique=True, null=False, max_length=255)
    name = models.CharField(null=False, max_length=255)
    credit_card_num = models.PositiveIntegerField(null=False)
    address = models.CharField(null=False, max_length=255)
    phone_num = models.PositiveIntegerField(null=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_su = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()