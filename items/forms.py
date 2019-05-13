import datetime

from django import forms
from django.contrib.admin import widgets
from django.forms import SplitDateTimeField
from django.forms.widgets import SplitDateTimeWidget

from .models import Item, ItemApplication, ItemFixedPrice, ItemBidPrice


class AddItemForm(forms.ModelForm):
    class Meta:
        model = ItemApplication
        fields = ['title', 'key_words', 'picture']


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['key_words', 'picture']


class SellItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['sellType']
        SELL_CHOICES = (
            ('', 'Sale type'),
            ('Fixed Price', 'Fixed Price'),
            ('Auction', 'Auction'),
        )
        widgets = {
            'sellType': forms.Select(choices=SELL_CHOICES, attrs={'class': 'form-control'}),
        }


class FixedPriceForm(forms.ModelForm):
    class Meta:
        model = ItemFixedPrice
        fields = ['price']


class BidPriceForm(forms.ModelForm):
    endDate = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], widget=forms.widgets.DateTimeInput(attrs={'placeholder': "DD/MM/YY HH:MM:SS"}))

    class Meta:
        model = ItemBidPrice
        fields = ['startPrice', 'endDate']

