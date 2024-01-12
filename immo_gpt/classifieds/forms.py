from django import forms
from tinymce.widgets import TinyMCE
from django.utils.translation import gettext as _
from .models import Home, Classified, Style

class AddHomeForm(forms.ModelForm): 
  name = forms.CharField(widget=forms.TextInput(attrs={
    "placeholder": _("Name")}))
  
  surface = forms.FloatField(widget=forms.TextInput(attrs={
    "type": "number",
    "placeholder": _("Surface -m2")
  }))
  
  price = forms.FloatField(widget=forms.TextInput(attrs={
    "type": "number",
    "placeholder": _("Price")
    }))

  class Meta:
    model = Home
    fields = ['name', 'price', 'surface']

class AddFirstDescription(forms.ModelForm):
  

  class Meta:
    model = Classified

    fields = ['text']
    # widgets = {
    #         'text': forms.Textarea(attrs={'spellcheck': 'true', 'rows': 5})
    #     }
    widgets = {'text': TinyMCE(attrs={'cols': 80, 'rows': 30})}


class AddEditStyle(forms.ModelForm):
  

  class Meta:
    model = Style

    fields = ['short_description', 'long_description']
    widgets = {
      'long_description': TinyMCE(attrs={'cols': 80, 'rows': 30}),
      'short_description': forms.TextInput(attrs={
    "placeholder": _("Title")}),
      }

                         