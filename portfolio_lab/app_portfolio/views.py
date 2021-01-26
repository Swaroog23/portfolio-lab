from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib import messages

from app_portfolio.forms import LoginForm, RegistrationForm
from app_portfolio.models import Category, Donation, Institution


class LandingPageView(View):
    def get(self, request):
        donated_bags = Donation.objects.count()
        institutions = Institution.objects.all()
        ctx = {"donated_bags": donated_bags, "institutions": institutions}
        return render(request, "index.html", ctx)


class DonationFormView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {"categories": categories, "institutions": institutions}
        return render(request, "form.html", ctx)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            login_function = LoginView.login_user(request, form)
            if login_function == 0:
                successfull_login_redirect = request.GET.get("next")
                if successfull_login_redirect:
                    return redirect(successfull_login_redirect)
                return redirect("/")
            elif login_function == 1:
                return redirect("/login/")
            else:
                return redirect("/register/")

        else:
            messages.add_message(
                request, messages.WARNING, "Proszę podać poprawny email"
            )
            return redirect("/login/")

    @staticmethod
    def login_user(request, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return 0
        elif user is None and User.objects.filter(email=email).exists():
            messages.add_message(request, messages.WARNING, "Zły email lub hasło")
            return 1
        else:
            messages.add_message(
                request, messages.WARNING, "Nie ma takiego użytkownika"
            )
            return 2


class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if RegisterView.register_user(request, form):
            return redirect("/login/")
        return redirect("/register/")

    @staticmethod
    def register_user(request, form):
        if form.is_valid():
            first_name = form.cleaned_data["name"]
            last_name = form.cleaned_data["surname"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            password2 = form.cleaned_data["password2"]
            if password == password2 and not User.objects.filter(email=email).exists():
                User.objects.create_user(
                    # Username for user is given email address
                    username=email,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                )

                return True
            elif User.objects.filter(email=email).exclude():
                messages.add_message(
                    request, messages.WARNING, "Podany email jest już zajęty!"
                )
                return False
            else:
                messages.add_message(
                    request, messages.WARNING, "Hasła nie są identyczne"
                )
                return False
        else:
            messages.add_message(request, messages.WARNING, "Niepoprawny email")
            return False
