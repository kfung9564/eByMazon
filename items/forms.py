from django import forms
from .models import Item

class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'key_words', 'is_biddable', 'picture']

    # def is_valid(self):
    #     form = super(AddItemForm, self).is_valid()
    #