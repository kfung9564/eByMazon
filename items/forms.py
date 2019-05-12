from django import forms
from .models import Item, ItemApplication


class AddItemForm(forms.ModelForm):
    class Meta:
        model = ItemApplication
        fields = ['title', 'key_words', 'picture']
