import datetime

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


class EventAddForm(forms.Form):
    title = forms.CharField(
        label='عنوان رویداد',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان ...'}),
    )
    event_date = forms.DateTimeField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'datetime', 'data-ha-datetimepicker': '#datetime'}),
        label="زمان رویداد ")

