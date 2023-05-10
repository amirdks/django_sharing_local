from django import forms
from django.core.exceptions import ValidationError

from account_module.models import User
from account_module.validation import is_valid_iran_code


class LoginForm(forms.Form):
    email = forms.EmailField(label='ایمیل', widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput(), label='رمز عبور')


class RegisterForm(forms.Form):
    email = forms.EmailField(label='ایمیل', widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput(), label='رمز عبور')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='تکرار رمز عبور')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password1 = cleaned_data.get("password1")
        if password != password1:
            return forms.ValidationError("پسورد یک با پسورد دو هماهنگ نیستند")
        return cleaned_data


class UserCreateForm(forms.Form):
    full_name = forms.CharField(
        label='نام و نام خانوادگی',
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "نام و نام خانوادگی ..."})
    )
    national_code = forms.CharField(
        label='کد ملی',
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "کد ملی ..."})
    )
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "ایمیل ..."})
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "رمزعبور ..."})
    )
    avatar = forms.ImageField(
        label='تصویر پروفایل',
        widget=forms.ClearableFileInput(),
        required=False
    )
    is_superuser = forms.BooleanField(
        label='دسترسی ادمین',
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False
    )

    def clean_national_code(self):
        value = self.cleaned_data.get("national_code")
        try:
            is_valid_iran_code(value)
        except ValidationError as e:
            forms.ValidationError(e)
        try:
            User.objects.get(national_code__exact=value)
            raise forms.ValidationError("کد ملی وارد شده تکراری میباشد")
        except User.DoesNotExist:
            return value

    def clean_national_code(self):
        value = self.cleaned_data.get("national_code")


class UserEditForm(forms.Form):
    full_name = forms.CharField(
        required=False,
        label='نام و نام خانوادگی',
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "نام و نام خانوادگی ..."})
    )
    national_code = forms.CharField(
        label='کد ملی',
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "کد ملی ..."}),
    )
    email = forms.EmailField(
        required=False,
        label='ایمیل',
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "ایمیل ..."})
    )
    password = forms.CharField(
        required=False,
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "رمزعبور ..."})
    )
    avatar = forms.ImageField(
        label='تصویر پروفایل',
        widget=forms.ClearableFileInput(),
        required=False,
    )

    def clean_national_code(self):
        value = self.cleaned_data.get("national_code")
        try:
            is_valid_iran_code(value)
        except ValidationError as e:
            forms.ValidationError(e)
        try:
            User.objects.get(national_code__exact=value)
            raise forms.ValidationError("کد ملی وارد شده تکراری میباشد")
        except User.DoesNotExist:
            return value
