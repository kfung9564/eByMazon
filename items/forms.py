import datetime

from django import forms
from django.contrib.admin import widgets
from django.forms import SplitDateTimeField
from django.forms.widgets import SplitDateTimeWidget
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from .models import Item, ItemApplication, ItemFixedPrice, ItemBidPrice


class AddItemForm(forms.ModelForm):
    class Meta:
        model = ItemApplication
        fields = ['title', 'key_words', 'description', 'picture']


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['key_words', 'description', 'picture']


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
    endDate = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'minDate': (
                    datetime.date.today()
                ).strftime(
                    '%Y-%m-%d'
                ),  # Today
                'useCurrent': True,
                'collapse': True,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )

    class Meta:
        model = ItemBidPrice
        fields = ['startPrice', 'endDate']

