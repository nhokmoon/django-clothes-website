from django import forms

from apps.home.models import Product


from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
CATEGORIES = (
    ('Fashion', 'Fashion'),
    ('Electronics', 'Electronics'),
    ('Home', 'Home'),
    ('Kitchen', 'Kitchen'),
)

SIZES = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
)

CURRENCIES = (
    ('USD', 'United States Dollar'),
    ('EUR', 'Euro'),
    ('GBP', 'British Pound'),
    ('INR', 'Indian Rupee'),
)


class ProductForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,

        widget=forms.TextInput(
            attrs={
                "placeholder": "name",
                "class": "form-control"
            }
        )
    )
    weight = forms.DecimalField(

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
                "id": "floatingTextarea2",
                "style": "height: 130px"
            }
        ))
    category = forms.ChoiceField(choices=CATEGORIES, widget=forms.Select(
        attrs={
            "placeholder": "Choose category",
            "class": "form-control"
        }
    ))
    size = forms.ChoiceField(choices=SIZES, widget=forms.Select(
        attrs={
            "placeholder": "Choose size",
            "class": "form-control"
        }
    ))
    currency = forms.ChoiceField(choices=CURRENCIES, widget=forms.Select(
        attrs={
            "placeholder": "Choose currency",
            "class": "form-control"
        }
    ))
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'onchange': 'readURL(this);',
            'accept': 'image/gif, image/jpeg, image/png',
            'id': 'formFile',
            'class': 'form-control',
        })
    )
    shoppee_link = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'https://...', 'onfocus': 'focused(this)', 'onfocusout': 'defocused(this)'}))
    facebook_link = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'https://...', 'onfocus': 'focused(this)', 'onfocusout': 'defocused(this)'}))
    instagram_link = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'https://...', 'onfocus': 'focused(this)', 'onfocusout': 'defocused(this)'}))

    price = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "99.00",
                "class": "form-control",
                "onfocus": "focused(this)",
                "onfocusout": "defocused(this)"
            }
        ))
    sku = forms.CharField(
        label='SKU',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '71283476591',
                'onfocus': 'focused(this)',
                'onfocusout': 'defocused(this)',
            }
        ))

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'weight', 'category', 'size',
                  'image', 'shoppee_link', 'facebook_link', 'instagram_link', 'currency', 'sku', 'price']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }
