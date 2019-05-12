from django.contrib import admin
from items.models import Item, ItemApplication, Blacklist

# Register your models here.

admin.site.register(Item)
admin.site.register(ItemApplication)
admin.site.register(Blacklist)