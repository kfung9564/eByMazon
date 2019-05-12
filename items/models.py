from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ItemApplication(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(primary_key=True, null=False, max_length=255)
    key_words = models.CharField(null=True, max_length=255)
    picture = models.URLField(null=False)


# Generic Item;
class Item(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(primary_key=True, null=False, max_length=255)
    key_words = models.CharField(null=True, max_length=255)
    picture = models.URLField(null=False)

    def __str__(self):
        return self.title


class Blacklist(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(primary_key=True, null=False, max_length=255)