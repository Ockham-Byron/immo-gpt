from django import forms
from django.utils.translation import gettext as _
from .models import Home

class AddHomeForm(forms.ModelForm): 
  name = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'form-control',
    'placeholder':_('Name'),
    })),
  
  price = forms.FloatField(widget=forms.TextInput(attrs={
    'type': 'number',
    'class': 'form-control',
    'placeholder': 'Price',
    })),

  class Meta:
    model = Home
    fields = ['name', 'price']
                         