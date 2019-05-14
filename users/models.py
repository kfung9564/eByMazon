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
    state = models.CharField(null=False, default="New York", max_length=255)
    phone_num = models.PositiveIntegerField(null=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(null=False, default="", max_length=255)
    credit_card_num = models.PositiveIntegerField(null=False, default=0)
    address = models.CharField(null=False, default="", max_length=255)
    state = models.CharField(null=False, default="New York", max_length=255)
    phone_num = models.PositiveIntegerField(null=False, default=0)
    is_new = models.BooleanField(default=True)
    is_su = models.BooleanField(default=False)

    def __str__(self):
        return self.user


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

        if instance.is_superuser:
            instance.profile.is_su = True
            instance.profile.is_new = False
            instance.profile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
