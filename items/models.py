from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Generic Sellable Item; No Bidding Involved
class Item(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(null=False, max_length=255)
    key_words = models.CharField(null=True, max_length=255)
    is_biddable = models.BooleanField(default=False)
    picture = models.URLField(null=False)

    def __str__(self):
        return self.title
