from django.shortcuts import render, redirect
from items.models import Item
from items.forms import AddItemForm
from django.contrib import messages
from users.decorators import su_required

# Create your views here.


def catalog(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST)
        if form.is_valid():
            suggested = form.save(commit=False)
            suggested.seller = request.user
            if request.user.profile.is_su:
                suggested.make_available()
            suggested.save()
            if request.user.profile.is_su:
                messages.success(request, 'New item added.')
            else:
                messages.success(request, 'Item has been sent to suggestions.')
            return redirect('index')
    else:
        form = AddItemForm()

    items = Item.objects.filter(is_available=True)

    content = {'items': items,
               'form': form}
    return render(request, 'items/catalog.html', content)


@su_required
def catalogreview(request):
    if request.method == 'POST':
        item_name = request.POST['item_name']
        item = Item.objects.get(title=item_name)
        if request.POST['confirmation'] == 'Approve':
            item.make_available()
            messages.success(request, item_name + ' has been added to the Catalog.')
        else:
            item.mark_blacklisted()

            messages.success(request, item_name + ' has been added to the Blacklist.')
        item.save()

    items = Item.objects.filter(is_available=False, is_blacklisted=False)
    content = {'items': items,}
    return render(request, 'items/catalogreview.html', content)


@su_required
def catalogblacklist(request):


    items = Item.objects.filter(is_available=False, is_blacklisted=True)
    content = {'items': items, }
    return render(request, 'items/catalogblacklist.html', content)
