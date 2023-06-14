import re

from django import forms

from account_module.models import AdministrativeDepartment, AdministrativeDepartmentHead
from contact_module.models import UnusualContactReason, ContactFormModel


def validate_mobile(value):
    regex = r"^(\+98|0)?9\d{9}$"
    matched = re.match(regex, value)
    is_match = bool(matched)
    return is_match


class ContactForm(forms.Form):
    # agent = forms.CharField(max_length=255, widget=forms.TextInput(), label="نام ایجنت پاسخو")
    phone_number = forms.CharField(
        max_length=13,
        widget=forms.TextInput(),
        label="شماره تلفن همراه"
    )
    unusual_contact_reason = forms.ModelChoiceField(
        queryset=UnusualContactReason.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="دلیل تماس غیر متعارف"
    )
    head_administrative_department = forms.ModelChoiceField(
        queryset=AdministrativeDepartmentHead.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="ارسال به سرپرست",
        help_text="درصورت نیاز به ارسال به سرپرست تمامی بخش ها این قسمت را خالی بگذارید *"
    )
    description = forms.CharField(
        widget=forms.Textarea(),
        label="توضیحات"
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        validate = validate_mobile(phone_number)
        if not validate:
            raise forms.ValidationError("شماره تلفن وارد شده معتبر نمیباشد")
        return phone_number


class ContactFormModelForm(forms.ModelForm):
    class Meta:
        model = ContactFormModel
        fields = ["title", "unusual_contact_reason", "users"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "unusual_contact_reason": forms.SelectMultiple(attrs={"class": "form-control", "multiple": "", "aria-label": "multiple select example"}),
            "users": forms.SelectMultiple(attrs={"class": "form-control", "multiple": "", "aria-label": "multiple select example"}),
        }
