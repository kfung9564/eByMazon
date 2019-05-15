from django import forms
from .models import UserApplication, Profile
from phonenumber_field.formfields import PhoneNumberField
from .models import UserApplication


class UserUpdateForm(forms.ModelForm):
    phone_num = PhoneNumberField()

    class Meta:
        model = Profile
        fields = ['credit_card_num', 'address', 'state', 'phone_num']
        labels = {
            'credit_card_num': 'Credit Card Number',
            'phone_num': 'Phone Number',
        }

        STATE_CHOICES = (
                    (("Alabama", "Alabama"),
                     ("Alaska", "Alaska"),
                     ("Arizona", "Arizona"),
                     ("Arkansas", "Arkansas"),
                     ("California", "California"),
                     ("Colorado", "Colorado"),
                     ("Connecticut", "Connecticut"),
                     ("Delaware", "Delaware"),
                     ("Florida", "Florida"),
                     ("Georgia", "Georgia"),
                     ("Hawaii", "Hawaii"),
                     ("Idaho", "Idaho"),
                     ("Illinois", "Illinois"),
                     ("Indiana", "Indiana"),
                     ("Iowa", "Iowa"),
                     ("Kansas", "Kansas"),
                     ("Kentucky", "Kentucky"),
                     ("Louisiana", "Louisiana"),
                     ("Maine", "Maine"),
                     ("Maryland", "Maryland"),
                     ("Massachusetts", "Massachusetts"),
                     ("Michigan", "Michigan"),
                     ("Minnesota", "Minnesota"),
                     ("Mississippi", "Mississippi"),
                     ("Missouri", "Missouri"),
                     ("Montana", "Montana"),
                     ("Nebraska", "Nebraska"),
                     ("Nevada", "Nevada"),
                     ("New Hampshire", "New Hampshire"),
                     ("New Jersey", "New Jersey"),
                     ("New Mexico", "New Mexico"),
                     ("New York", "New York"),
                     ("North Carolina", "North Carolina"),
                     ("North Dakota", "North Dakota"),
                     ("Ohio", "Ohio"),
                     ("Oklahoma", "Oklahoma"),
                     ("Oregon", "Oregon"),
                     ("Pennsylvania", "Pennsylvania"),
                     ("Rhode Island", "Rhode Island"),
                     ("South Carolina", "South Carolina"),
                     ("South Dakota", "South Dakota"),
                     ("Tennessee", "Tennessee"),
                     ("Texas", "Texas"),
                     ("Utah", "Utah"),
                     ("Vermont", "Vermont"),
                     ("Virginia", "Virginia"),
                     ("Washington", "Washington"),
                     ("West Virginia", "West Virginia"),
                     ("Wisconsin", "Wisconsin"),
                     ("Wyoming", "Wyoming"))
                )
        widgets = {
         'state': forms.Select(choices=STATE_CHOICES, attrs={'class': 'form-control'}),
        }


class UserAppForm(forms.ModelForm):
    phone_num = PhoneNumberField()

    class Meta:
        model = UserApplication
        fields = ['username', 'name', 'credit_card_num', 'address', 'state', 'phone_num']
        labels = {
            'credit_card_num': 'Credit Card Number',
            'phone_num': 'Phone Number',
        }

        STATE_CHOICES = (
            (("Alabama", "Alabama"),
             ("Alaska", "Alaska"),
             ("Arizona", "Arizona"),
             ("Arkansas", "Arkansas"),
             ("California", "California"),
             ("Colorado", "Colorado"),
             ("Connecticut", "Connecticut"),
             ("Delaware", "Delaware"),
             ("Florida", "Florida"),
             ("Georgia", "Georgia"),
             ("Hawaii", "Hawaii"),
             ("Idaho", "Idaho"),
             ("Illinois", "Illinois"),
             ("Indiana", "Indiana"),
             ("Iowa", "Iowa"),
             ("Kansas", "Kansas"),
             ("Kentucky", "Kentucky"),
             ("Louisiana", "Louisiana"),
             ("Maine", "Maine"),
             ("Maryland", "Maryland"),
             ("Massachusetts", "Massachusetts"),
             ("Michigan", "Michigan"),
             ("Minnesota", "Minnesota"),
             ("Mississippi", "Mississippi"),
             ("Missouri", "Missouri"),
             ("Montana", "Montana"),
             ("Nebraska", "Nebraska"),
             ("Nevada", "Nevada"),
             ("New Hampshire", "New Hampshire"),
             ("New Jersey", "New Jersey"),
             ("New Mexico", "New Mexico"),
             ("New York", "New York"),
             ("North Carolina", "North Carolina"),
             ("North Dakota", "North Dakota"),
             ("Ohio", "Ohio"),
             ("Oklahoma", "Oklahoma"),
             ("Oregon", "Oregon"),
             ("Pennsylvania", "Pennsylvania"),
             ("Rhode Island", "Rhode Island"),
             ("South Carolina", "South Carolina"),
             ("South Dakota", "South Dakota"),
             ("Tennessee", "Tennessee"),
             ("Texas", "Texas"),
             ("Utah", "Utah"),
             ("Vermont", "Vermont"),
             ("Virginia", "Virginia"),
             ("Washington", "Washington"),
             ("West Virginia", "West Virginia"),
             ("Wisconsin", "Wisconsin"),
             ("Wyoming", "Wyoming"))
        )
        widgets = {
            'state': forms.Select(choices=STATE_CHOICES, attrs={'class': 'form-control'}),
        }
