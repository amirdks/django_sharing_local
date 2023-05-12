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
        widget=forms.TextInput(attrs={'class': '', 'placeholder': 'عنوان ...'}),
    )
    event_date = forms.DateField(widget=forms.TextInput(
        attrs={'class': '', 'id': 'datetime', 'data-ha-datetimepicker': '#datetime'}),
        label="زمان رویداد ")

    def clean_event_date(self):
        # end_time = self.cleaned_data.get("event_date")
        # end_time_str = end_time.strftime("%m/%d/%Y %H:%M:%S")
        # end_time = end_time.strptime(end_time_str, "%m/%d/%Y %H:%M:%S")
        end_time = self.cleaned_data.get('event_date')

        end_time_str = end_time.strftime("%m/%d/%Y")
        # end_time = end_time.strptime(end_time_str, "%m/%d/%Y %H:%M:%S")
        return end_time


class BirthdayCreateForm(forms.Form):
    text = forms.CharField(max_length=255, widget=forms.TextInput(attrs={"class": ""}), label="متن تولد")
    user = forms.ModelChoiceField(widget=forms.Select(attrs={"class": "form-control", "style": "width:50%;"}),
                                  label="برای کاربر",
                                  queryset=User.objects.all())
    birthday_date = forms.DateField(widget=forms.TextInput(
        attrs={'class': '', 'id': 'datetime', 'data-ha-datetimepicker': '#datetime'}), label="تاریخ تولد")

    def clean_birthday_date(self):
        # end_time = self.cleaned_data.get("event_date")
        # end_time_str = end_time.strftime("%m/%d/%Y %H:%M:%S")
        # end_time = end_time.strptime(end_time_str, "%m/%d/%Y %H:%M:%S")
        birthday_date = self.cleaned_data.get('birthday_date')

        birthday_str = birthday_date.strftime("%m/%d/%Y")
        # end_time = end_time.strptime(end_time_str, "%m/%d/%Y %H:%M:%S")
        return birthday_date
