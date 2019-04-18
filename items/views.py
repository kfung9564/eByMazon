from django.shortcuts import render
from items.models import Item

# Create your views here.


def catalog(request):
    items = Item.objects.all()
    return render(request, 'items/catalog.html', {'items': items})
