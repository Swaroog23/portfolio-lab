from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models.lookups import In
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib import messages


from app_portfolio.forms import LoginForm, RegistrationForm, DonationForm
from app_portfolio.models import Category, Donation, Institution


def dontaion_form_confirmation_view(request):
    return render(request, "form-confirmation.html")


@login_required
def user_detail_view(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, "user-details.html", {"user": user})


class LandingPageView(View):
    def get(self, request):
        donated_bags = Donation.objects.count()
        ctx = {"donated_bags": donated_bags}
        return render(request, "index.html", ctx)


class DonationFormView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        form = DonationForm()
        ctx = {"form": form}
        return render(request, "form.html", ctx)

    def post(self, request, user_id):
        form = DonationForm(request.POST)
        user = User.objects.get(pk=user_id)
        if (
            form.is_valid()
            and request.POST.get("categories")
            and request.POST.get("organization")
        ):
            try:
                DonationFormView.get_form_data_and_create_donation(request, form, user)
            except ValidationError:
                messages.add_message(
                    request, messages.WARNING, "Data nie może być z przeszłości!"
                )
                return render(request, "form.html", {"form": DonationForm()})
            return redirect("/donation_confirmed/")
        messages.add_message(
            request, messages.WARNING, "Wystąpił błąd, wypełnij formularz ponownie"
        )
        return render(request, "form.html", {"form": DonationForm()})

    @staticmethod
    def get_form_data_and_create_donation(request, form, user):
        chosen_categories = request.POST.getlist("categories")
        amount_of_bags = int(form.cleaned_data["amount_of_bags"])
        chosen_organization = request.POST.get("organization")
        street = form.cleaned_data["street"]
        city = form.cleaned_data["city"]
        postal_code = form.cleaned_data["postal_code"]
        phone_number = int(form.cleaned_data["phone_number"])
        pickup_date = form.cleaned_data["pickup_date"]
        pickup_time = form.cleaned_data["pickup_time"]
        additional_pickup_information = form.cleaned_data[
            "additional_pickup_information"
        ]
        try:
            new_donation = Donation()
            new_donation.quantity = amount_of_bags
            new_donation.institution = Institution.objects.get(
                pk=int(chosen_organization)
            )
            new_donation.address = street
            new_donation.phone_number = phone_number
            new_donation.city = city
            new_donation.zip_code = postal_code
            new_donation.pick_up_date = pickup_date
            new_donation.pick_up_time = pickup_time
            new_donation.pick_up_comment = additional_pickup_information
            new_donation.user = user
            new_donation.save()
            for item in chosen_categories:
                new_donation.categories.add(Category.objects.get(pk=int(item)))
            new_donation.save()
            return new_donation
        except ValidationError as err:
            raise ValidationError("Data nie może być z przeszłości!")


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
