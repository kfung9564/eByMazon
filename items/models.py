from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


def validate_date(date):
    if date < datetime.now():
        raise ValidationError("The date cannot be in the past!")


class ItemApplication(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(primary_key=True, null=False, max_length=255)
    key_words = models.CharField(null=True, max_length=255)
    picture = models.URLField(null=False)


# Generic Item;
class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(primary_key=True, null=False, max_length=255)
    key_words = models.CharField(null=True, max_length=255)
    picture = models.URLField(null=False)
    sellType = models.CharField(default='Offsale', max_length=255)
    uploadDate = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title


class Blacklist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(primary_key=True, null=False, max_length=255)


class ItemFixedPrice(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0.01)])


class Order(models.Model):
    item = models.ForeignKey(ItemFixedPrice, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    orderDate = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        unique_together = (("item", "buyer"),)


class ItemBidPrice(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    startPrice = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0.01)])
    startDate = models.DateTimeField(default=datetime.now, blank=True)
    endDate = models.DateTimeField(validators=[validate_date])


class Bid(models.Model):
    item = models.ForeignKey(ItemBidPrice, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bidPrice = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0.01)])
    bidDate = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        unique_together = (("item", "bidder", "bidPrice"),)

