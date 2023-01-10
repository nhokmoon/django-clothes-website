from django import forms

from apps.home.models import Product


from django.core.validators import MinValueValidator, MaxValueValidator,RegexValidator

class ProductForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255, 
        validators=[
            MinValueValidator(5),
            MaxValueValidator(255),
            RegexValidator(
                regex='^[A-Za-z0-9 ]*$',
                message='Product name should only contain letters, numbers and spaces.'
            )
        ],
        widget=forms.TextInput(
            attrs={
                "placeholder": "name",
                "class": "form-control"
            }
        )
    )
    weight = forms.DecimalField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        widget=forms.TextInput(
            attrs={
                "placeholder": "weight",
                "class": "form-control"
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "description",
                "class": "form-control",
                "id":"floatingTextarea2",
                "style":"height: 130px"
            }
        ))
    class Meta:
        model = Product
        fields = ['name', 'weight', 'description']
        widgets = {
            'user': forms.HiddenInput()
        }
