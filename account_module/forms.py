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
    birthday_date = forms.DateField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'datetime', 'data-ha-datetimepicker': '#datetime'}), label="تاریخ تولد")

    is_superuser = forms.BooleanField(
        label='دسترسی ادمین',
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False
    )

    def clean_birthday_date(self):
        birthday_date = self.cleaned_data.get('birthday_date')
        birthday_str = birthday_date.strftime("%m/%d/%Y")
        return birthday_date

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


# class UserEditForm(forms.Form):
#     full_name = forms.CharField(
#         required=False,
#         label='نام و نام خانوادگی',
#         widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "نام و نام خانوادگی ..."})
#     )
#     national_code = forms.CharField(
#         label='کد ملی',
#         widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "کد ملی ..."}),
#     )
#     email = forms.EmailField(
#         required=False,
#         label='ایمیل',
#         widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "ایمیل ..."})
#     )
#     password = forms.CharField(
#         required=False,
#         label='رمز عبور',
#         widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "رمزعبور ..."})
#     )
#     birthday_date = forms.DateField(widget=forms.TextInput(
#         attrs={'class': 'form-control', 'id': 'datetime', 'data-ha-datetimepicker': '#datetime'}), label="تاریخ تولد")
#
#     avatar = forms.ImageField(
#         label='تصویر پروفایل',
#         widget=forms.ClearableFileInput(),
#         required=False,
#     )
#
#     def clean_national_code(self):
#         value = self.cleaned_data.get("national_code")
#         try:
#             is_valid_iran_code(value)
#         except ValidationError as e:
#             forms.ValidationError(e)
#         try:
#             User.objects.get(national_code__exact=value)
#             raise forms.ValidationError("کد ملی وارد شده تکراری میباشد")
#         except User.DoesNotExist:
#             return value
#
#     def clean_birthday_date(self):
#         birthday_date = self.cleaned_data.get('birthday_date')
#         birthday_str = birthday_date.strftime("%m/%d/%Y")
#         return birthday_date


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["full_name", "national_code", "email", "password", "birthday_date", "avatar"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "نام و نام خانوادگی ..."}),
            "national_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "کد ملی ..."}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "ایمیل ..."}),
            "password": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "رمزعبور ..."}),
            "birthday_date": forms.TextInput(
                attrs={'class': 'form-control', 'id': 'datetime', 'data-ha-datetimepicker': '#datetime'}),
            "avatar": forms.ClearableFileInput(),
        }
        labels = {
            "full_name": "نام و نام خانوادگی",
            "national_code": "کد ملی",
            "email": 'ایمیل',
            "password": 'ایمیل',
            "birthday_date": 'تاریخ تولد',
            "avatar": 'تصویر آواتار',
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(UserEditForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['full_name'].required = False
        self.fields['email'].required = False
        self.fields['password'].required = False
        self.fields['avatar'].required = False

    # def clean_national_code(self):
    #     value = self.cleaned_data.get("national_code")
        # try:
        #     is_valid_iran_code(value)
        # except ValidationError as e:
        #     forms.ValidationError(e)
        # try:
        #     User.objects.get(national_code__exact=value)
        #     raise forms.ValidationError("کد ملی وارد شده تکراری میباشد")
        # except User.DoesNotExist:
        #     return value

    def clean_birthday_date(self):
        birthday_date = self.cleaned_data.get('birthday_date')
        # birthday_str = birthday_date.strftime("%m/%d/%Y")
        return birthday_date
