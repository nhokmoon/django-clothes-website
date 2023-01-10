from itertools import product
from django import forms


class ProductForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ['name', 'price', 'description']
        widgets = {
            'user': forms.HiddenInput()
        }
