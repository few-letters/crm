from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.html import format_html
from .models import Customer, Product, OrderItem, Order


User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "User name"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email address"}),
            "password1": forms.PasswordInput(attrs={"placeholder": "Password"}),
            "password2": forms.PasswordInput(attrs={"placeholder": "Confirm password"}),
        }

        labels = {field: "" for field in fields}

        help_texts = {
            "username": format_html("<span class='ms-1'>Letters, digits and @/./+/-/_ only.</span>"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Один цикл замість десятка однакових рядків
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


class AddCustomerForm(forms.ModelForm):
    class Meta:
            model = Customer

            fields = ("first_name", "last_name", "email", "phone", "country", "region", "city", "address")

            widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name", "class": "form-control"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name", "class": "form-control"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email address", "class": "form-control"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone", "class": "form-control"}),
            "country": forms.TextInput(attrs={"placeholder": "Country", "class": "form-control"}),
            "region": forms.TextInput(attrs={"placeholder": "Region", "class": "form-control"}),
            "city": forms.TextInput(attrs={"placeholder": "City", "class": "form-control"}),
            "address": forms.TextInput(attrs={"placeholder": "Address", "class": "form-control"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price', 'step': '1'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Name',
            'price': 'Price (₴)',
            'description': 'Description',
            'image': 'Product Image',
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'status']
        
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select status-select'}),
        }


OrderItemFormSet = inlineformset_factory(
    parent_model=Order,
    model=OrderItem,
    fields=('product', 'quantity', 'price'),
    widgets={
        'product': forms.Select(attrs={'class': 'form-select'}), 
        'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
    },
    extra=0,
    can_delete=True,
    min_num=1,
    validate_min=True
)