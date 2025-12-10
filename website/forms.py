from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # specify which fields of model will be used in form
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

        # to render fields in HTML
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "User name",
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "First name",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Last name",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email address",
            }),
            "password1": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Password",
            }),
            "password2": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Confirm password",
            }),
        }

        # get rid of labels
        labels = {
            "username": "",
            "first_name": "",
            "last_name": "",
            "email": "",
            "password1": "",
            "password2": "",
        }

        # if help_text is needed
        help_texts = {
            "username": "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
            "password1": "Your password must contain at least 8 characters and not be too common.",
            "password2": "Enter the same password as before, for verification.",
        }
