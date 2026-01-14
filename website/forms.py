from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.html import format_html
from .models import Record


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


class AddRecordForm(forms.ModelForm):
    class Meta:
            model = Record

            fields = ("first_name", "last_name", "email", "phone", "state", "city")

            widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name", "class": "form-control"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name", "class": "form-control"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email address", "class": "form-control"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone", "class": "form-control"}),
            "state": forms.TextInput(attrs={"placeholder": "State", "class": "form-control"}),
            "city": forms.TextInput(attrs={"placeholder": "City", "class": "form-control"}),
        }
