import decimal
from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Avg
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from items.models import Item, ItemApplication, Blacklist, ItemFixedPrice, ItemBidPrice, Order, Bid
from items.forms import AddItemForm, EditItemForm, SellItemForm, FixedPriceForm, BidPriceForm, NotFirstJustifyForm, \
    PlaceBidForm
from django.contrib import messages
from users.decorators import su_required

# Create your views here.
from users.forms import RatingForm
from users.models import UserMessages, Transaction, Rating


def search(request):
    if request.method == 'GET':
        title = request.GET.get('search')
        # keywords = request.GET.get('search')
        # fixedPrice = request.GET.get('search')
        # ratings = request.GET.get('search')

        item = Item.objects.get(title=request.GET['Title'])
        itemSearched = Item.objects.filter(item=title)

        content = {'items': itemSearched
                    }
        return render(request,"search.html", content)
    else:
        messages.success(request, "No items found")
        return render(request,"search.html",{})



def catalog(request):
    fixedPriceItems = ItemFixedPrice.objects.all()
    bidPriceItems = ItemBidPrice.objects.all()

    content = {'fixedPriceItems': fixedPriceItems,
               'bidPriceItems': bidPriceItems}
    return render(request, 'items/catalog.html', content)


def processorders(request):
    item = Item.objects.get(title=request.GET['Title'])
    fixedItem = ItemFixedPrice.objects.get(item=item)
    orders = Order.objects.filter(item=fixedItem).order_by('orderDate')
    firstOrder = orders.first()

    content = {'orders': orders,
               'firstOrder': firstOrder,
               'item': item}
    return render(request, 'items/processorders.html', content)


def confirmorder(request):
    stateTax = {
        "Alabama": 4,
        "Alaska": 0,
        "Arizona": 5.6,
        "Arkansas": 6.5,
        "California": 7.25,
        "Colorado": 2.9,
        "Connecticut": 6.35,
        "Delaware": 0,
        "Florida": 6,
        "Georgia": 4,
        "Hawaii": 4,
        "Idaho": 6,
        "Illinois": 6.25,
        "Indiana": 7,
        "Iowa": 6,
        "Kansas": 6.5,
        "Kentucky": 6,
        "Louisiana": 4.45,
        "Maine": 5.5,
        "Maryland": 6,
        "Massachusetts": 6.25,
        "Michigan": 6,
        "Minnesota": 6.875,
        "Mississippi": 7,
        "Missouri": 4.225,
        "Montana": 0,
        "Nebraska": 5.5,
        "Nevada": 6.85,
        "New Hampshire": 0,
        "New Jersey": 6.625,
        "New Mexico": 5.125,
        "New York": 4,
        "North Carolina": 4.75,
        "North Dakota": 5,
        "Ohio": 5.75,
        "Oklahoma": 4.5,
        "Oregon": 0,
        "Pennsylvania": 6,
        "Rhode Island": 7,
        "South Carolina": 6,
        "South Dakota": 4.5,
        "Tennessee": 7,
        "Texas": 6.25,
        "Utah": 4.85,
        "Vermont": 6,
        "Virginia": 4.3,
        "Washington": 6.5,
        "West Virginia": 6,
        "Wisconsin": 5,
        "Wyoming": 4
    }

    item = Item.objects.get(title=request.GET['Title'])
    buyer = User.objects.get(username=request.GET['Buyer'])

    fixedItem = ItemFixedPrice.objects.get(item=item)
    order = Order.objects.get(item=fixedItem, buyer=buyer)

    if request.method == 'POST':
        if request.POST['Confirm'] == 'Confirm':
            item.sellType = 'Offsale'
            item.owner = order.buyer
            item.save()
            fixedItem.delete()

            tax = round(
                decimal.Decimal(stateTax.get(buyer.profile.state))
                * decimal.Decimal(0.01)
                * decimal.Decimal(fixedItem.price),
                2)
            totalPrice = round(tax + decimal.Decimal(fixedItem.price), 2)

            if buyer.profile.is_vip:
                totalPrice = round(decimal.Decimal(totalPrice) * decimal.Decimal(0.95), 2)

            Transaction.objects.create(seller=request.user.username,
                                       buyer=buyer.username,
                                       title=item.title,
                                       sellType='Fixed Price',
                                       originalPrice=fixedItem.price,
                                       paidPrice=totalPrice)

            buyer.profile.spent = round(decimal.Decimal(buyer.profile.spent) + decimal.Decimal(totalPrice), 2)
            buyer.profile.save()

            if buyer.profile.spent > 500:
                buyer.profile.is_vip = True
                buyer.profile.save()

            messages.success(request, item.title + ' has been sold to ' + item.owner.profile.name + '.')
        return redirect('itemmanager')

    content = {'order': order,
               'item': item}
    return render(request, 'items/confirmorder.html', content)


def confirmnotfirst(request):
    stateTax = {
        "Alabama": 4,
        "Alaska": 0,
        "Arizona": 5.6,
        "Arkansas": 6.5,
        "California": 7.25,
        "Colorado": 2.9,
        "Connecticut": 6.35,
        "Delaware": 0,
        "Florida": 6,
        "Georgia": 4,
        "Hawaii": 4,
        "Idaho": 6,
        "Illinois": 6.25,
        "Indiana": 7,
        "Iowa": 6,
        "Kansas": 6.5,
        "Kentucky": 6,
        "Louisiana": 4.45,
        "Maine": 5.5,
        "Maryland": 6,
        "Massachusetts": 6.25,
        "Michigan": 6,
        "Minnesota": 6.875,
        "Mississippi": 7,
        "Missouri": 4.225,
        "Montana": 0,
        "Nebraska": 5.5,
        "Nevada": 6.85,
        "New Hampshire": 0,
        "New Jersey": 6.625,
        "New Mexico": 5.125,
        "New York": 4,
        "North Carolina": 4.75,
        "North Dakota": 5,
        "Ohio": 5.75,
        "Oklahoma": 4.5,
        "Oregon": 0,
        "Pennsylvania": 6,
        "Rhode Island": 7,
        "South Carolina": 6,
        "South Dakota": 4.5,
        "Tennessee": 7,
        "Texas": 6.25,
        "Utah": 4.85,
        "Vermont": 6,
        "Virginia": 4.3,
        "Washington": 6.5,
        "West Virginia": 6,
        "Wisconsin": 5,
        "Wyoming": 4
    }

    item = Item.objects.get(title=request.GET['Title'])
    buyer = User.objects.get(username=request.GET['Buyer'])

    fixedItem = ItemFixedPrice.objects.get(item=item)
    order = Order.objects.get(item=fixedItem, buyer=buyer)

    firstOrder = Order.objects.filter(item=fixedItem).order_by('orderDate')[:1].get()

    System = User.objects.get(username='System')

    if request.method == 'POST':
        form = NotFirstJustifyForm(request.POST)

        if form.is_valid():
            if request.POST['Confirm'] == 'Confirm':
                msg = 'Your ' + item.title + ' order was denied due to the following reasons: ' + request.POST.get('message')
                UserMessages.objects.create(sender=System, recipient=firstOrder.buyer, title='Order Denied', message=msg)

                tax = round(
                    decimal.Decimal(stateTax.get(buyer.profile.state))
                    * decimal.Decimal(0.01)
                    * decimal.Decimal(fixedItem.price),
                    2)
                totalPrice = round(tax + decimal.Decimal(fixedItem.price), 2)

                if buyer.profile.is_vip:
                    totalPrice = round(decimal.Decimal(totalPrice)*decimal.Decimal(0.95), 2)

                Transaction.objects.create(seller=request.user.username,
                                           buyer=buyer.username,
                                           title=item.title,
                                           sellType='Fixed Price',
                                           originalPrice=fixedItem.price,
                                           paidPrice=totalPrice)

                buyer.profile.spent = round(decimal.Decimal(buyer.profile.spent) + decimal.Decimal(totalPrice), 2)
                buyer.profile.save()

                if buyer.profile.spent > 500:
                    buyer.profile.is_vip = True
                    buyer.profile.save()

                item.sellType = 'Offsale'
                item.owner = order.buyer
                item.save()
                fixedItem.delete()

                messages.success(request, item.title + ' has been sold to ' + item.owner.profile.name + '.')

                return redirect('itemmanager')

    else:
        form = NotFirstJustifyForm()

    content = {'order': order,
               'item': item,
               'form': form}
    return render(request, 'items/confirmnotfirst.html', content)


def fixeditempage(request):
    item = Item.objects.get(title=request.GET['Title'])
    fixedPriceItem = ItemFixedPrice.objects.get(item=item)

    content = {'fixedPriceItem': fixedPriceItem}
    return render(request, 'items/fixeditempage.html', content)


def fixeditemorder(request):
    stateTax = {
        "Alabama": 4,
        "Alaska": 0,
        "Arizona": 5.6,
        "Arkansas": 6.5,
        "California": 7.25,
        "Colorado": 2.9,
        "Connecticut": 6.35,
        "Delaware": 0,
        "Florida": 6,
        "Georgia": 4,
        "Hawaii": 4,
        "Idaho": 6,
        "Illinois": 6.25,
        "Indiana": 7,
        "Iowa": 6,
        "Kansas": 6.5,
        "Kentucky": 6,
        "Louisiana": 4.45,
        "Maine": 5.5,
        "Maryland": 6,
        "Massachusetts": 6.25,
        "Michigan": 6,
        "Minnesota": 6.875,
        "Mississippi": 7,
        "Missouri": 4.225,
        "Montana": 0,
        "Nebraska": 5.5,
        "Nevada": 6.85,
        "New Hampshire": 0,
        "New Jersey": 6.625,
        "New Mexico": 5.125,
        "New York": 4,
        "North Carolina": 4.75,
        "North Dakota": 5,
        "Ohio": 5.75,
        "Oklahoma": 4.5,
        "Oregon": 0,
        "Pennsylvania": 6,
        "Rhode Island": 7,
        "South Carolina": 6,
        "South Dakota": 4.5,
        "Tennessee": 7,
        "Texas": 6.25,
        "Utah": 4.85,
        "Vermont": 6,
        "Virginia": 4.3,
        "Washington": 6.5,
        "West Virginia": 6,
        "Wisconsin": 5,
        "Wyoming": 4
    }

    item = Item.objects.get(title=request.GET['Title'])
    fixedPriceItem = ItemFixedPrice.objects.get(item=item)
    censoredCardNum = '************' + request.user.profile.credit_card_num[12:]
    tax = round(decimal.Decimal(stateTax.get(request.user.profile.state)) * decimal.Decimal(0.01) * fixedPriceItem.price, 2)
    totalPrice = round(tax + fixedPriceItem.price, 2)

    if request.user.profile.is_vip:
        totalPrice = round(decimal.Decimal(totalPrice) * decimal.Decimal(0.95), 2)

    if request.method == 'POST':
        if request.POST['Order'] == 'Place Order':
            if not Order.objects.filter(item=fixedPriceItem, buyer=request.user):
                Order.objects.create(item=fixedPriceItem, buyer=request.user)
                messages.success(request, 'Order for ' + fixedPriceItem.item.title + ' complete.')
            else:
                messages.success(request, 'You have already ordered ' + fixedPriceItem.item.title + '.')
        else:
            messages.success(request, 'Order for ' + fixedPriceItem.item.title + ' canceled.')

        return redirect('catalog')

    content = {'fixedPriceItem': fixedPriceItem,
               'censoredCardNum': censoredCardNum,
               'totalPrice': totalPrice,
               'tax': tax}
    return render(request, 'items/orderitem.html', content)


def biditempage(request):
    item = Item.objects.get(title=request.GET['Title'])
    bidPriceItem = ItemBidPrice.objects.get(item=item)

    content = {'bidPriceItem': bidPriceItem}
    return render(request, 'items/biditempage.html', content)


def placebidpage(request):
    stateTax = {
        "Alabama": 4,
        "Alaska": 0,
        "Arizona": 5.6,
        "Arkansas": 6.5,
        "California": 7.25,
        "Colorado": 2.9,
        "Connecticut": 6.35,
        "Delaware": 0,
        "Florida": 6,
        "Georgia": 4,
        "Hawaii": 4,
        "Idaho": 6,
        "Illinois": 6.25,
        "Indiana": 7,
        "Iowa": 6,
        "Kansas": 6.5,
        "Kentucky": 6,
        "Louisiana": 4.45,
        "Maine": 5.5,
        "Maryland": 6,
        "Massachusetts": 6.25,
        "Michigan": 6,
        "Minnesota": 6.875,
        "Mississippi": 7,
        "Missouri": 4.225,
        "Montana": 0,
        "Nebraska": 5.5,
        "Nevada": 6.85,
        "New Hampshire": 0,
        "New Jersey": 6.625,
        "New Mexico": 5.125,
        "New York": 4,
        "North Carolina": 4.75,
        "North Dakota": 5,
        "Ohio": 5.75,
        "Oklahoma": 4.5,
        "Oregon": 0,
        "Pennsylvania": 6,
        "Rhode Island": 7,
        "South Carolina": 6,
        "South Dakota": 4.5,
        "Tennessee": 7,
        "Texas": 6.25,
        "Utah": 4.85,
        "Vermont": 6,
        "Virginia": 4.3,
        "Washington": 6.5,
        "West Virginia": 6,
        "Wisconsin": 5,
        "Wyoming": 4
    }

    item = Item.objects.get(title=request.GET['Title'])
    bidPriceItem = ItemBidPrice.objects.get(item=item)
    censoredCardNum = '************' + request.user.profile.credit_card_num[12:]

    if datetime.now() >= bidPriceItem.endDate:
        messages.success(request, 'Bidding for ' + bidPriceItem.item.title + ' has already ended.')
        return redirect('catalog')

    bids = Bid.objects.filter(item=bidPriceItem).order_by('-bidPrice')
    if not bids:
        highest = bidPriceItem.startPrice
    else:
        highest = bids.first().bidPrice

    if request.method == 'POST':
        form = PlaceBidForm(request.POST)

        if request.POST['Bid'] == 'Place Bid':
            if decimal.Decimal(request.POST.get('bidPrice')) <= highest:
                form = PlaceBidForm()

                messages.success(request, 'Bid price must be higher than current highest!')
                content = {'highest': highest,
                           'form': form,
                           'bidPriceItem': bidPriceItem,
                           'censoredCardNum': censoredCardNum}
                return render(request, 'items/placebidpage.html', content)

            else:
                Bid.objects.create(item=bidPriceItem, bidder=request.user, bidPrice=request.POST.get('bidPrice'))

                messages.success(request, 'Bid for ' + bidPriceItem.item.title + ' successfully placed!')

        elif request.POST['Bid'] == 'Check Tax':
            form = PlaceBidForm(initial={'bidPrice': request.POST.get('bidPrice')})
            tax = round(
                decimal.Decimal(stateTax.get(request.user.profile.state)) * decimal.Decimal(0.01) * decimal.Decimal(request.POST.get(
                    'bidPrice')),
                2)
            totalPrice = round(tax + decimal.Decimal(request.POST.get('bidPrice')), 2)

            if request.user.profile.is_vip:
                totalPrice = round(decimal.Decimal(totalPrice) * decimal.Decimal(0.95), 2)
                messages.success(request, "Total price after " + request.user.profile.state +
                                 " state tax and VIP discount is: " + str(
                    totalPrice))
            else:
                messages.success(request, "Total price after " + request.user.profile.state + " state tax is: " + str(
                    totalPrice))

            content = {'highest': highest,
                       'form': form,
                       'bidPriceItem': bidPriceItem,
                       'censoredCardNum': censoredCardNum}
            return render(request, 'items/placebidpage.html', content)
        else:
            messages.success(request, 'Bid for ' + bidPriceItem.item.title + ' canceled.')

        return redirect('catalog')
    else:
        form = PlaceBidForm()

    content = {'highest': highest,
               'form': form,
               'bidPriceItem': bidPriceItem,
               'censoredCardNum': censoredCardNum}
    return render(request, 'items/placebidpage.html', content)


def processbids(request):
    item = Item.objects.get(title=request.GET['Title'])
    bidItem = ItemBidPrice.objects.get(item=item)
    bids = Bid.objects.filter(item=bidItem).order_by('-bidPrice')

    winner = None
    if bids.count() == 1:
        winner = bids.first()
    elif bids.count() > 1:
        winner = bids[1]

    content = {'bids': bids,
               'winner': winner,
               'item': item}
    return render(request, 'items/processbids.html', content)


def confirmwinner(request):
    stateTax = {
        "Alabama": 4,
        "Alaska": 0,
        "Arizona": 5.6,
        "Arkansas": 6.5,
        "California": 7.25,
        "Colorado": 2.9,
        "Connecticut": 6.35,
        "Delaware": 0,
        "Florida": 6,
        "Georgia": 4,
        "Hawaii": 4,
        "Idaho": 6,
        "Illinois": 6.25,
        "Indiana": 7,
        "Iowa": 6,
        "Kansas": 6.5,
        "Kentucky": 6,
        "Louisiana": 4.45,
        "Maine": 5.5,
        "Maryland": 6,
        "Massachusetts": 6.25,
        "Michigan": 6,
        "Minnesota": 6.875,
        "Mississippi": 7,
        "Missouri": 4.225,
        "Montana": 0,
        "Nebraska": 5.5,
        "Nevada": 6.85,
        "New Hampshire": 0,
        "New Jersey": 6.625,
        "New Mexico": 5.125,
        "New York": 4,
        "North Carolina": 4.75,
        "North Dakota": 5,
        "Ohio": 5.75,
        "Oklahoma": 4.5,
        "Oregon": 0,
        "Pennsylvania": 6,
        "Rhode Island": 7,
        "South Carolina": 6,
        "South Dakota": 4.5,
        "Tennessee": 7,
        "Texas": 6.25,
        "Utah": 4.85,
        "Vermont": 6,
        "Virginia": 4.3,
        "Washington": 6.5,
        "West Virginia": 6,
        "Wisconsin": 5,
        "Wyoming": 4
    }

    item = Item.objects.get(title=request.GET['Title'])
    bid = Bid.objects.get(pk=request.GET['Bid'])
    bidder = User.objects.get(username=bid.bidder)

    bidItem = ItemBidPrice.objects.get(item=item)

    if request.method == 'POST':
        if request.POST['Confirm'] == 'Confirm':
            tax = round(
                decimal.Decimal(stateTax.get(bidder.profile.state))
                * decimal.Decimal(0.01)
                * decimal.Decimal(bid.bidPrice),
                2)
            totalPrice = round(tax + decimal.Decimal(bid.bidPrice), 2)

            if bidder.profile.is_vip:
                totalPrice = round(decimal.Decimal(totalPrice) * decimal.Decimal(0.95), 2)

            Transaction.objects.create(seller=request.user.username,
                                       buyer=bidder.username,
                                       title=item.title,
                                       sellType='Auction',
                                       originalPrice=bid.bidPrice,
                                       paidPrice=totalPrice)

            bidder.profile.spent = round(decimal.Decimal(bidder.profile.spent) + decimal.Decimal(totalPrice), 2)
            bidder.profile.save()

            if bidder.profile.spent > 500:
                bidder.profile.is_vip = True
                bidder.profile.save()

            item.sellType = 'Offsale'
            item.owner = bidder
            item.save()
            bidItem.delete()

            messages.success(request, item.title + ' has been sold to ' + item.owner.profile.name + '.')
        return redirect('itemmanager')

    content = {'bid': bid,
               'item': item}
    return render(request, 'items/confirmwinner.html', content)


def confirmnotwinner(request):
    stateTax = {
        "Alabama": 4,
        "Alaska": 0,
        "Arizona": 5.6,
        "Arkansas": 6.5,
        "California": 7.25,
        "Colorado": 2.9,
        "Connecticut": 6.35,
        "Delaware": 0,
        "Florida": 6,
        "Georgia": 4,
        "Hawaii": 4,
        "Idaho": 6,
        "Illinois": 6.25,
        "Indiana": 7,
        "Iowa": 6,
        "Kansas": 6.5,
        "Kentucky": 6,
        "Louisiana": 4.45,
        "Maine": 5.5,
        "Maryland": 6,
        "Massachusetts": 6.25,
        "Michigan": 6,
        "Minnesota": 6.875,
        "Mississippi": 7,
        "Missouri": 4.225,
        "Montana": 0,
        "Nebraska": 5.5,
        "Nevada": 6.85,
        "New Hampshire": 0,
        "New Jersey": 6.625,
        "New Mexico": 5.125,
        "New York": 4,
        "North Carolina": 4.75,
        "North Dakota": 5,
        "Ohio": 5.75,
        "Oklahoma": 4.5,
        "Oregon": 0,
        "Pennsylvania": 6,
        "Rhode Island": 7,
        "South Carolina": 6,
        "South Dakota": 4.5,
        "Tennessee": 7,
        "Texas": 6.25,
        "Utah": 4.85,
        "Vermont": 6,
        "Virginia": 4.3,
        "Washington": 6.5,
        "West Virginia": 6,
        "Wisconsin": 5,
        "Wyoming": 4
    }

    item = Item.objects.get(title=request.GET['Title'])
    bid = Bid.objects.get(pk=request.GET['Bid'])
    bidder = User.objects.get(username=bid.bidder)

    bidItem = ItemBidPrice.objects.get(item=item)

    bids = Bid.objects.filter(item=bidItem).order_by('-bidPrice')
    winner = None
    if bids.count() == 1:
        winner = bids.first()
    elif bids.count() > 1:
        winner = bids[1]

    System = User.objects.get(username='System')

    if request.method == 'POST':
        form = NotFirstJustifyForm(request.POST)

        if form.is_valid():
            if request.POST['Confirm'] == 'Confirm':
                msg = 'Your ' + item.title + ' bid was denied due to the following reasons: ' + request.POST.get('message')
                UserMessages.objects.create(sender=System, recipient=winner.bidder, title='Bid Denied', message=msg)

                tax = round(
                    decimal.Decimal(stateTax.get(bidder.profile.state))
                    * decimal.Decimal(0.01)
                    * decimal.Decimal(bid.bidPrice),
                    2)
                totalPrice = round(tax + decimal.Decimal(bid.bidPrice), 2)

                if bidder.profile.is_vip:
                    totalPrice = round(decimal.Decimal(totalPrice)*decimal.Decimal(0.95), 2)

                Transaction.objects.create(seller=request.user.username,
                                           buyer=bidder.username,
                                           title=item.title,
                                           sellType='Auction',
                                           originalPrice=bid.bidPrice,
                                           paidPrice=totalPrice)

                bidder.profile.spent = round(decimal.Decimal(bidder.profile.spent) + decimal.Decimal(totalPrice), 2)
                bidder.profile.save()

                if bidder.profile.spent > 500:
                    bidder.profile.is_vip = True
                    bidder.profile.save()

                item.sellType = 'Offsale'
                item.owner = bidder
                item.save()
                bidItem.delete()

                messages.success(request, item.title + ' has been sold to ' + item.owner.profile.name + '.')

                return redirect('itemmanager')
    else:
        form = NotFirstJustifyForm()

    content = {'bid': bid,
               'item': item,
               'form': form}
    return render(request, 'items/confirmnotwinner.html', content)


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

    if item.sellType == 'Fixed':
        itemOnMarket = ItemFixedPrice.objects.filter(item=item)
        itemOnMarket.delete()
    else:
        itemOnMarket = ItemBidPrice.objects.filter(item=item)
        itemOnMarket.delete()

    item.sellType = 'Offsale'
    item.save()

    messages.success(request, item.title + ' has been put off sale.')
    return redirect('itemmanager')


def rateuser(request):
    seller = User.objects.get(username=request.GET['Username'])
    rater = request.user

    if request.method == 'POST':
        rateform = RatingForm(request.POST)
        if rateform.is_valid():
            Rating.objects.create(seller=seller, rater=rater, grade=request.POST['grade'], comment=request.POST['comment'])

            distinctRating = Rating.objects.filter(seller=seller).values('rater').distinct()
            if distinctRating.count() >= 3:
                if distinctRating.aggregate(Avg('grade')) >= 4:
                    seller.profile.is_vip = True
                    seller.profile.save()

            messages.success(request, "Rating submitted!")
            return redirect('index')
    else:
        rateform = RatingForm()

    content = {'rateform': rateform,
               'seller': seller}
    return render(request, 'users/rateuser.html', content)


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

