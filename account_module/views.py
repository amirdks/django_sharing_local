from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from account_module.forms import LoginForm, RegisterForm
from account_module.models import *


# Create your views here.
class LoginView(View):
    def get(self, request: HttpRequest):
        # TODO : add redirect to home view
        if request.user.is_authenticated:
            return redirect(reverse("home_view"))
        form = LoginForm()
        context = {
            "form": form
        }
        return render(request, "account_module/login.html", context)

    def post(self, request):
        # TODO : add redirect to home view
        if request.user.is_authenticated:
            pass
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            user = User.objects.filter(email__exact=email).first()
            if user:
                is_password_correct = user.check_password(password)
                if is_password_correct:
                    login(request, user)
                    UserLoggedIn.objects.create(user_id=user.id)
                    return redirect(reverse("home_view"))
                else:
                    login_form.add_error(field='password', error='کلمه عبور اشتباه است')
            else:
                login_form.add_error(field='email', error='کاربری با مشخصات وارد شده یافت نشد')
        return render(request, 'account_module/login.html', context={"form": login_form})


class RegisterView(View):
    def get(self, request):
        # TODO : add redirect to home view
        if request.user.is_authenticated:
            return redirect(reverse("home_view"))
        form = RegisterForm()
        context = {
            "form": form
        }
        return render(request, "account_module/register.html", context)

    def post(self, request):
        # TODO : add redirect to home view
        if request.user.is_authenticated:
            pass
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            old_user = User.objects.filter(email__iexact=email).first()
            if not old_user:
                password = form.cleaned_data.get("password")
                user = User.objects.create_user(email=email, password=password)
                return redirect(reverse("login_view"))
            else:
                form.add_error("email", "کاربری قبلا با این ایمیل ثبت نام کرده است")
        return render(request, 'account_module/register.html', context={"form": form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('home_view'))
        UserLoggedOut.objects.create(user_id=request.user.id)
        logout(request)
        return redirect(reverse('login_view'))
