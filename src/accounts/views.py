from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

class UserLoginView(LoginView):
    template_name = "accounts/auth/login.html"
    authentication_form = AuthenticationForm
