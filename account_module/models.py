import datetime

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
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
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
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
    national_code = models.CharField(max_length=10, null=True, unique=True, validators=[is_valid_iran_code])
    birthday_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to="images/avatar")
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["full_name", "national_code", "email"]

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def get_reaming_days(self):
        if self.birthday_date:
            res = self.birthday_date - timezone.now().date()
            return f"{res.days} روز"
        else:
            return "هنوز ست نشده"

    @property
    def reaming_date(self):
        return self.birthday_date - timezone.now().date()


class UserLoggedIn(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.full_name


class UserLoggedOut(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.full_name
