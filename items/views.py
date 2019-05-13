from django.shortcuts import render, redirect
from items.models import Item, ItemApplication, Blacklist
from items.forms import AddItemForm, EditItemForm
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
                Item.objects.create(owner=request.POST.get('owner'), title=request.POST.get('title'),
                                    key_words=request.POST.get('key_words'), picture=request.POST.get('picture'))
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
    ownedItems = Item.objects.filter(owner=request.user)

    content = {'ownedItems': ownedItems}
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
