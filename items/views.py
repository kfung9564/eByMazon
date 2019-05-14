from django.shortcuts import render, redirect
from django.urls import reverse

from items.models import Item, ItemApplication, Blacklist, ItemFixedPrice, ItemBidPrice
from items.forms import AddItemForm, EditItemForm, SellItemForm, FixedPriceForm, BidPriceForm
from django.contrib import messages
from users.decorators import su_required

# Create your views here.


def catalog(request):
    items = Item.objects.all()

    content = {'items': items}
    return render(request, 'items/catalog.html', content)


def apply(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST)

        isValid = True
        if Blacklist.objects.filter(title=request.POST['title']).exists():
            messages.success(request, 'Invalid item.')
            isValid = False
        else:
            if Item.objects.filter(title=request.POST['title']).exists():
                messages.success(request, 'Item already exists.')
                isValid = False

        if form.is_valid() and isValid:
            if request.user.profile.is_su:
                Item.objects.create(owner=request.user, title=request.POST.get('title'),
                                    key_words=request.POST.get('key_words'), description=request.POST.get('description'),
                                    picture=request.POST.get('picture'))
                messages.success(request, 'New item added.')
            else:
                application = form.save(commit=False)
                application.owner = request.user
                application.save()

                messages.success(request, 'Item has been sent to for review.')
            return redirect('index')
    else:
        form = AddItemForm()

    content = {'form': form}
    return render(request, 'items/apply.html', content)


def manageitems(request):
    ownedOffsaleItems = Item.objects.filter(owner=request.user, sellType='Offsale')
    ownedFixedItems = Item.objects.filter(owner=request.user, sellType='Fixed')
    ownedBidItems = Item.objects.filter(owner=request.user, sellType='Bid')

    content = {'ownedOffsaleItems': ownedOffsaleItems,
               'ownedFixedItems': ownedFixedItems,
               'ownedBidItems': ownedBidItems}
    return render(request, 'items/itemmanager.html', content)


def edititems(request):
    item = Item.objects.get(title=request.GET['Title'])
    form = EditItemForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        messages.success(request, "Item information successfully updated!")

        return redirect('itemmanager')

    content = {'form': form,
               'item': item}
    return render(request, 'items/edititem.html', content)


def sellitems(request):
    item = Item.objects.get(title=request.GET['Title'])
    item_param = '{}?Title='+item.title
    typeForm = SellItemForm(request.POST or None, instance=item)

    if typeForm.is_valid():
        typeForm.save(commit=False)

        if request.POST['sellType'] == 'Fixed Price':
            return redirect(item_param.format(reverse('sellfixed')))
        elif request.POST['sellType'] == 'Auction':
            return redirect(item_param.format(reverse('sellbid')))

    content = {'typeForm': typeForm,
               'item': item}
    return render(request, 'items/sellitems.html', content)


def sellfixed(request):
    item = Item.objects.get(title=request.GET['Title'])

    if request.method == 'POST':
        fixedForm = FixedPriceForm(request.POST)

        if fixedForm.is_valid():
            fixedItem = fixedForm.save(commit=False)
            item.sellType = 'Fixed'
            item.save()
            fixedItem.item = item
            fixedItem.save()

            messages.success(request, item.title+' has been put up for sale at a fixed price.')
            return redirect('itemmanager')
    else:
        fixedForm = FixedPriceForm()

    content = {'fixedForm': fixedForm,
               'item': item}
    return render(request, 'items/putupforfixeditem.html', content)


def sellbid(request):
    item = Item.objects.get(title=request.GET['Title'])

    if request.method == 'POST':
        bidForm = BidPriceForm(request.POST)

        if bidForm.is_valid():
            bidItem = bidForm.save(commit=False)
            item.sellType = 'Bid'
            item.save()
            bidItem.item = item
            bidItem.save()

            messages.success(request, item.title + ' has been put up for bidding.')
            return redirect('itemmanager')
    else:
        bidForm = BidPriceForm()

    content = {'bidForm': bidForm,
               'item': item}
    return render(request, 'items/putupbiditem.html', content)


def putoffsale(request):
    item = Item.objects.get(title=request.GET['Title'])
    item.sellType = 'Offsale'
    item.save()

    if item.sellType == 'Fixed':
        itemOnMarket = ItemFixedPrice.objects.filter(item=item)
        itemOnMarket.delete()
    else:
        itemOnMarket = ItemBidPrice.objects.filter(item=item)
        itemOnMarket.delete()

    messages.success(request, item.title + ' has been put offsale.')
    return redirect('itemmanager')


@su_required
# review applications
def catalogreview(request):
    apps = ItemApplication.objects.all()

    if request.method == 'POST':
        item_name = request.POST['item_name']
        application = ItemApplication.objects.get(title=item_name)

        if request.POST['confirmation'] == 'Approve':
            Item.objects.create(owner=application.owner, title=application.title,
                                key_words=application.key_words, picture=application.picture)

            messages.success(request, item_name + ' has been approved and added to the Catalog.')
        else:
            # add to blacklist
            Blacklist.objects.create(owner=application.owner, title=application.title)
            messages.success(request, item_name + ' has been denied and added to the Blacklist.')

        application.delete()

    content = {'apps': apps}
    return render(request, 'items/catalogreview.html', content)


@su_required
def catalogblacklist(request):
    blacklist = Blacklist.objects.all()
    content = {'blacklist': blacklist, }
    return render(request, 'items/catalogblacklist.html', content)


@su_required
def itemlist(request):
    items = Item.objects.all()

    content = {'items': items}
    return render(request, 'items/allitemlist.html', content)


@su_required
def removeitem(request):
    item = Item.objects.get(title=request.GET['Title'])
    if request.method == 'POST':
        if request.POST['Delete'] == 'Confirm':
            item_name = item.title
            Blacklist.objects.create(owner=item.owner, title=item.title)
            item.delete()

            messages.success(request, item_name + ' has been deleted and added to the Blacklist.')
        return redirect('itemlist')

    content = {'item': item}
    return render(request, 'items/removeitem.html', content)


@su_required
def su_edititem(request):
    item = Item.objects.get(title=request.GET['Title'])
    form = EditItemForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        messages.success(request, "Item information successfully updated!")

        return redirect('itemlist')

    content = {'form': form,
               'item': item}
    return render(request, 'items/suedititem.html', content)

