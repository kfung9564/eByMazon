from django.db import models
from django.contrib.auth.models import User

# Create your models here.


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
    isForSale = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Blacklist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(primary_key=True, null=False, max_length=255)


class ItemOnMarket(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    sellType = models.CharField(max_length=255)
    postDate = models.DateField()


class ItemFixedPrice(models.Model):
    item = models.ForeignKey(ItemOnMarket, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()


class Order(models.Model):
    item = models.ForeignKey(ItemFixedPrice, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    orderDate = models.DateField()

    class Meta:
        unique_together = (("item", "buyer"),)


class ItemBidPrice(models.Model):
    item = models.ForeignKey(ItemOnMarket, on_delete=models.CASCADE)
    startPrice = models.PositiveIntegerField()
    duration = models.TimeField()


class Bid(models.Model):
    item = models.ForeignKey(ItemBidPrice, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bidPrice = models.PositiveIntegerField()
    bidDate = models.DateField()

    class Meta:
        unique_together = (("item", "bidder", "bidPrice"),)