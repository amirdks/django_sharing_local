from django import forms


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
