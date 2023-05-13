from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from account_module.forms import LoginForm, RegisterForm, UserCreateForm, UserEditForm
from account_module.mixins import JustSuperUser
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


class UserListView(JustSuperUser, View):
    def get(self, request):
        context = {
            'users': User.objects.all().exclude(id=request.user.id).order_by("-is_superuser")
        }
        return render(request, 'account_module/user-list.html', context)


class UserCreateView(JustSuperUser, View):
    def get(self, request):
        form = UserCreateForm()
        context = {
            "form": form,
        }
        return render(request, "account_module/user-create.html", context)

    def post(self, request):
        form = UserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data.pop("email")
            password = form.cleaned_data.pop("password")
            is_superuser = form.cleaned_data.get("is_superuser")
            try:
                if is_superuser:

                    new_user = User.objects.create_superuser(email, password, **form.cleaned_data)
                else:
                    new_user = User.objects.create_user(email, password, **form.cleaned_data)
                return redirect(reverse("user_list_view"))
            except IntegrityError as e:
                form.add_error("email", "ایمیل و یا کد ملی وارد شده تکراری میباشد")
                form.add_error("national_code", "ایمیل و یا کد ملی وارد شده تکراری میباشد")
        context = {
            'form': form
        }
        return render(request, "account_module/user-create.html", context)


class UserDeleteView(JustSuperUser, View):
    http_method_names = ["get"]

    def get(self, request, pk):
        try:
            current_user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "کاربر مورد نظر یافت نشد"})
        if current_user.is_superuser:
            return JsonResponse({"status": "error", "message": "نمیتوانید کاربر با دسترسی ویژه را حذف کنید"})
        current_user.delete()
        return JsonResponse({"status": "success", "message": "کاربر با موفقیت حذف شد"})


class UserEditView(JustSuperUser, View):
    def get(self, request, pk):
        user: User = get_object_or_404(User, pk=pk, is_superuser=False)
        # user_init = {
        #     "full_name": user.full_name,
        #     "email": user.email,
        #     "national_code": user.national_code,
        #     "avatar": user.avatar,
        #     "birthday_date": user.birthday_date,
        # }
        form = UserEditForm(instance=user)
        context = {
            "user": user,
            "form": form,
        }
        return render(request, "account_module/user-edit.html", context)

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk, is_superuser=False)
        form = UserEditForm(request.POST, request.FILES, instance=user)
        print("valid")
        if form.is_valid():
            form.save()
            return redirect(reverse("user_list_view"))
        context = {
            "user": user,
            "form": form,
        }
        return render(request, "account_module/user-edit.html", context)


class CallLogView(JustSuperUser,View):
    def get(self, request):
        return render(request, "account_module/call-log.html")