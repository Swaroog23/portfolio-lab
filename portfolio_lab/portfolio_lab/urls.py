"""portfolio_lab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as django_auth_views

from app_portfolio.views import (
    LandingPageView,
    DonationFormView,
    LoginView,
    RegisterView,
    dontaion_form_confirmation_view,
    user_detail_view,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", LandingPageView.as_view(), name="index"),
    path("add_donation/<user_id>", DonationFormView.as_view(), name="add-donation"),
    path("donation_confirmed/", dontaion_form_confirmation_view, name="from-confirm"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", django_auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("user/<int:user_id>", user_detail_view, name="user-detail"),
]
