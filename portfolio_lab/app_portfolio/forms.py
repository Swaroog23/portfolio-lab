from django import forms
from django.core.validators import EmailValidator


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