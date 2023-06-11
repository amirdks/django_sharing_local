import datetime

from django.core.validators import URLValidator
from django.db import models
from django.utils import timezone


# Create your models here.

class File(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="files")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = 'قایل های ارسالی'
        verbose_name = 'فایل ارسالی'


class Event(models.Model):
    title = models.CharField(max_length=255)
    event_date = models.DateField()

    class Meta:
        ordering = ["event_date"]
        verbose_name_plural = 'رویداد ها'
        verbose_name = 'رویداد'

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
        verbose_name_plural = 'تولد ها'
        verbose_name = 'تولد'

    def reaming_date(self):
        return self.birthday_date - datetime.datetime.today().date()


class HyperLink(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/hyper_link")
    link = models.TextField(validators=[URLValidator()])
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'لینک خارجی'
        verbose_name_plural = 'لینک های خارجی'

    def __str__(self):
        return self.title
