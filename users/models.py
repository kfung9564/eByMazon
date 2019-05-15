from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator, MinValueValidator, \
    MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
from items.models import Item


class UserApplication(models.Model):
    username = models.CharField(unique=True, null=False, max_length=255)
    name = models.CharField(null=False, max_length=255)
    credit_card_num = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                r'^[0-9]*$',
            ),
            MinLengthValidator(16),
            MaxLengthValidator(16),
        ],
    )
    address = models.CharField(null=False, max_length=255)
    state = models.CharField(null=False, default="New York", max_length=255)
    phone_num = PhoneNumberField(null=False, blank=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(null=False, default="", max_length=255)
    credit_card_num = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                r'^[0-9]*$',
            ),
            MinLengthValidator(16),
            MaxLengthValidator(16),
        ],
    )
    address = models.CharField(null=False, default="", max_length=255)
    state = models.CharField(null=False, default="New York", max_length=255)
    phone_num = PhoneNumberField(null=False, blank=False)
    spent = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0.01)], default=0)
    is_vip = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    is_su = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class UserBlacklist(models.Model):
    username = models.CharField(primary_key=True, null=False, max_length=255)


class UserMessages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    title = models.CharField(null=True, max_length=255)
    message = models.TextField(null=True)
    date = models.DateTimeField(default=datetime.now, blank=True)


class Transaction(models.Model):
    seller = models.CharField(null=False, max_length=255)
    buyer = models.CharField(null=False, max_length=255)
    title = models.CharField(null=False, max_length=255)
    sellType = models.CharField(null=False, max_length=255)
    originalPrice = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0.01)])
    paidPrice = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0.01)])
    date = models.DateTimeField(default=datetime.now, blank=True)


class Rating(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rater')
    grade = models.DecimalField(default=0, max_digits=2, decimal_places=1, validators=[MaxValueValidator(5.1),
                                                                         MinValueValidator(-0.9)]
                                )
    comment = models.TextField(null=True)
    date = models.DateTimeField(default=datetime.now, blank=True)


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
