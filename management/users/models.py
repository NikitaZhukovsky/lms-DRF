from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime
from django.utils.timezone import now


class CustomUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError('Email field must be set')
        if not password:
            raise ValueError('Password field must be set')
        if not first_name:
            raise ValueError('First name field must be set')
        if not last_name:
            raise ValueError('Last name field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name_plural = "Users"

    ROLE_CHOICES = (
        ('User', 'User'),
        ('Student', 'Student'),
        ('Teacher', 'Teacher')
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True, default=None)
    last_name = models.CharField(max_length=100, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=False)
    role = models.CharField(choices=ROLE_CHOICES, max_length=50, default='User')
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

