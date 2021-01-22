from app_portfolio.models import Donation, Institution
from django.shortcuts import render
from django.views import View


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
        return render(request, "register.html")