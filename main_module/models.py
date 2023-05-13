import datetime

from django.db import models
from django.utils import timezone


# Create your models here.

class File(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="files")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class Event(models.Model):
    title = models.CharField(max_length=255)
    event_date = models.DateField()

    class Meta:
        ordering = ["event_date"]

    def get_reaming_days(self):
        res = self.event_date - timezone.now().date()
        return f"{res.days} روز"


class Birthday(models.Model):
    text = models.CharField(max_length=255)
    user = models.ForeignKey("account_module.User", on_delete=models.CASCADE)
    birthday_date = models.DateField()

    def get_reaming_days(self):
        if self.birthday_date:
            res = self.birthday_date - timezone.now().date()
            return f"{res.days} روز"
        else:
            return "هنوز ست نشده"

    class Meta:
        ordering = ["birthday_date"]

    def reaming_date(self):
        return self.birthday_date - datetime.datetime.today().date()
