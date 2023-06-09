import datetime

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from account_module.validation import is_valid_iran_code


# Create your models here.


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password and extra data.
        """
        if not email:
            raise ValueError(_("the Email must be set"))
        email = self.normalize_email(email)
        administrative_department = None
        administrative_department_head = None
        if extra_fields.get("administrative_department"):
            administrative_department = extra_fields.pop("administrative_department")
        if extra_fields.get("administrative_department_head"):
            administrative_department_head = extra_fields.pop("administrative_department_head")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        if administrative_department:
            user.administrative_department.set(administrative_department)
        if administrative_department_head:
            user.administrative_department_head.set(administrative_department_head)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model for authentication management through email address instead of username
    """
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    national_code = models.CharField(max_length=10, unique=True, validators=[is_valid_iran_code])
    birthday_date = models.DateField(null=True, blank=True)
    recruitment_date = models.DateField(null=True, blank=True)
    leaving_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to="images/avatar")
    administrative_department = models.ManyToManyField("AdministrativeDepartment", null=True, blank=True)
    administrative_department_head = models.ManyToManyField("AdministrativeDepartmentHead", null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "national_code"]

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return f"{self.email} ==> {self.full_name}"

    @property
    def get_reaming_days(self):
        if self.birthday_date:
            res = self.birthday_date.replace(year=timezone.now().date().year) - timezone.now().date()
            if res.days > 0:
                return f"{res.days} روز"
            elif res.days < 0:
                res = self.birthday_date.replace(year=timezone.now().date().year + 1) - timezone.now().date()
                return f"{res.days} روز"
            elif res.days == 0:
                return "امروز تولدشه"
        else:
            return "هنوز ست نشده"

    @property
    def is_today_birthday(self):
        if self.birthday_date:
            res = self.birthday_date.replace(year=timezone.now().date().year) - timezone.now().date()
            if res.days == 0:
                return True
            else:
                return False
        else:
            return False

    @property
    def reaming_date(self):
        return self.birthday_date - timezone.now().date()


class UserLoggedIn(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'گزارش ورود'
        verbose_name_plural = 'گزارشات ورود'

    def __str__(self):
        return self.user.full_name


class UserLoggedOut(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'گزارش خروح'
        verbose_name_plural = 'گزارشات خروج'

    def __str__(self):
        return self.user.full_name


class AdministrativeDepartment(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'دپارتمان اداری'
        verbose_name_plural = 'دپارتمان های اداری'

    def __str__(self):
        return self.title


class AdministrativeDepartmentHead(models.Model):
    administrative_department = models.OneToOneField("AdministrativeDepartment", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'سرپرست دپارتمان'
        verbose_name_plural = 'سرپرست های دپارتمان'

    def __str__(self):
        return self.administrative_department.title


@receiver(post_save, sender=AdministrativeDepartment)
def create_administrative_department_head(sender, instance, created, **kwargs):
    if created:
        AdministrativeDepartmentHead.objects.create(administrative_department=instance)
