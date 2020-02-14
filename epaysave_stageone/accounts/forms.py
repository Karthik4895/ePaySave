from django import forms
from .models import Profile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    username=forms.CharField(widget=forms.PasswordInput)
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta():
        model=User
        fields=('username','password')

class ProfileForm(forms.ModelForm):

    class Meta:
        model=Profile
        widgets = {
            'address_line_1': forms.TextInput(attrs={'placeholder': 'Door No,Building'}),
            'address_line_2': forms.TextInput(attrs={'placeholder': 'Area,Locality'}),
        }
        fields=('first_name','last_name','mobile_no','email','address_line_1','address_line_2','postal_code','city','country')




