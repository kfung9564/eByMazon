from django import forms
from .models import UserApplication


class UserAppForm(forms.ModelForm):
    class Meta:
        model = UserApplication
        fields = ['username', 'name', 'credit_card_num', 'address', 'phone_num']
        labels = {
            'credit_card_num': 'Credit Card Number',
            'phone_num': 'Phone Number',
        }

