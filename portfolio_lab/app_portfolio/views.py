import django
from django.contrib.auth.models import User
from app_portfolio.models import Donation, Institution
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import login
from django.contrib import messages


class LandingPage(View):
    def get(self, request):
        donated_bags = Donation.objects.count()
        institutions = Institution.objects.all()
        ctx = {"donated_bags": donated_bags, "institutions": institutions}
        return render(request, "index.html", ctx)


class AddDonation(View):
    def get(self, request):
        return render(request, "form.html")


class Login(View):
    def get(self, request):
        return render(request, "login.html")


class Register(View):
    def get(self, request):
        storage = messages.get_messages(request)
        for message in storage:
            del message
        return render(request, "register.html")

    def post(self, request):
        first_name = request.POST.get("name")
        last_name = request.POST.get("surname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if Register.register_user(
            request, first_name, last_name, email, password, password2
        ):
            return redirect("/login/")
        else:
            return redirect("/register/")

    @staticmethod
    def register_user(request, first_name, last_name, email, password, password2):
        if password == password2 and not User.objects.filter(email=email).exists():
            User.objects.create_user(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )

            return True
        elif User.objects.filter(email=email).exclude():
            messages.add_message(request, messages.WARNING, "Email is already taken")
            return False
        else:
            messages.add_message(request, messages.WARNING, "Passwords do not match")
            return False
