from django.contrib import admin
from items.models import Item, ItemApplication, Blacklist, ItemFixedPrice, Order, ItemBidPrice, Bid

# Register your models here.
from users.models import Transaction

admin.site.register(Item)
admin.site.register(ItemApplication)
admin.site.register(Blacklist)
admin.site.register(ItemFixedPrice)
admin.site.register(Order)
admin.site.register(ItemBidPrice)
admin.site.register(Bid)
admin.site.register(Transaction)
