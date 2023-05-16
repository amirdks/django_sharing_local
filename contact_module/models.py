from django.db import models


# Create your models here.
class UnusualContactReason(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Contact(models.Model):
    sender = models.ForeignKey('account_module.User', on_delete=models.CASCADE)
    agent = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=13, unique=True)
    unusual_contact_reason = models.ForeignKey('UnusualContactReason', on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sender.email
