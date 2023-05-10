import datetime

from django import forms

from account_module.models import User
from main_module.models import File, Event, Birthday


class FileAddForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["title", "file"]
        labels = {
            "title": "عنوان فایل",
            "file": "فایل"
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "add-file-title-input", "placeholder": "عنوان فایل ..."}),
            "file": forms.FileInput(attrs={"class": "add-file-input"})
        }


class EventAddForm(forms.Form):
    title = forms.CharField(
        label='عنوان رویداد',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان ...'}),
    )
    event_date = forms.DateTimeField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'datetime', 'data-ha-datetimepicker': '#datetime'}),
        label="زمان رویداد ")


class BirthdayCreateForm(forms.Form):
    text = forms.CharField(max_length=255, widget=forms.TextInput(attrs={"class": "form-control"}), label="متن تولد")
    user = forms.ModelChoiceField(widget=forms.Select(attrs={"class": "form-control"}), label="برای کاربر",
                                  queryset=User.objects.all())
    birthday_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"class": "form-control"}), label="تاریخ تولد")
