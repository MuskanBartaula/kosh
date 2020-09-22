from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

class UserLoginView(LoginView):
    template_name = "accounts/auth/login.html"
    authentication_form = AuthenticationForm

def logout_view(request):
    logout(request)
    return redirect('accounts:login')
