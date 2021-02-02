from django import forms
from django.core.validators import EmailValidator
from django.forms import widgets
from app_portfolio.models import Category, Institution


class RegistrationForm(forms.Form):
    name = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={"placeholder": "Imię"})
    )
    surname = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={"placeholder": "Nazwisko"})
    )
    email = forms.EmailField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Email"}),
        validators=[EmailValidator],
    )
    password = forms.CharField(
        max_length=150, widget=forms.PasswordInput(attrs={"placeholder": "Hasło"})
    )
    password2 = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput(attrs={"placeholder": "Powtórz hasło"}),
    )


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Email"}),
        validators=[EmailValidator],
    )
    password = forms.CharField(
        max_length=150, widget=forms.PasswordInput(attrs={"placeholder": "Hasło"})
    )


class DonationForm(forms.Form):
    amount_of_bags = forms.IntegerField(min_value=1, required=True)
    street = forms.CharField(max_length=150, required=True)
    city = forms.CharField(max_length=100, required=True)
    postal_code = forms.RegexField(regex="[0-9]{2}-[0-9]{3}", required=True)
    phone_number = forms.RegexField(regex="[0-9]{9}", required=True)
    pickup_date = forms.DateField(
        required=True, widget=forms.DateInput(attrs={"type": "date"})
    )
    pickup_time = forms.TimeField(
        required=True, widget=forms.TimeInput(attrs={"type": "time"})
    )
    additional_pickup_information = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "5"}), required=False
    )
