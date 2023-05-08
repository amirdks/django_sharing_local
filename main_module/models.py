import datetime

from django.db import models


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


class Birthday(models.Model):
    text = models.CharField(max_length=255)
    user = models.ForeignKey("account_module.User", on_delete=models.CASCADE)
    birthday_date = models.DateField()

    class Meta:
        ordering = ["birthday_date"]

    def reaming_date(self):
        return self.birthday_date - datetime.datetime.today().date()
