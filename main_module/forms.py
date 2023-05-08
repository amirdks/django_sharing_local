from django import forms

from main_module.models import File, Event


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


class EventAddForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "event_date"]
        labels = {
            "title": "عنوان رویداد",
            "event_date": "تاریخ رویداد"
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "add-file-title-input", "placeholder": "عنوان رویداد ..."}),
            "event_date": forms.TextInput(
                attrs={'class': 'form-control', 'id': 'datetime', 'data-ha-datetimepicker': '#datetime'}),
        }
