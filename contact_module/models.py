from django.db import models


# Create your models here.
class UnusualContactReason(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'دلیل ارتباط'
        verbose_name_plural = 'دلایل ارتباط'

    def __str__(self):
        return self.title


class Contact(models.Model):
    sender = models.ForeignKey('account_module.User', on_delete=models.CASCADE)
    # agent = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=13)
    unusual_contact_reason = models.ForeignKey('UnusualContactReason', on_delete=models.CASCADE)
    head_administrative_department = models.ForeignKey("account_module.AdministrativeDepartmentHead",
                                                       on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ارتباط کاربران'
        verbose_name_plural = 'ارتباطات کاربران'

    def __str__(self):
        return self.sender.email


class ContactReport(models.Model):
    image = models.ImageField(upload_to="images/matplotlib")
    date = models.DateTimeField(auto_now_add=True)
    is_stabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'گزارش ارتباط'
        verbose_name_plural = 'گزارشات ارتباط'
