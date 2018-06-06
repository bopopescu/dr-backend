from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, user_name='', password=None, is_superuser=False):
        if not email:
            raise ValueError("User must have an email address")

        now = timezone.now()
        user = self.model(email=self.normalize_email(email), user_name=user_name)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    user_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    avatar = models.FileField(upload_to='avatars/', null=True, blank=True)
    is_active = models.BooleanField(default= False)
    is_admin = models.BooleanField(default=False)
    specialization = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=300, blank=True)
    intro_text = models.CharField(max_length=300, blank=True)
    otp = models.CharField(max_length=300, blank=True)
    otp_expiration = models.DateTimeField(blank=True, null=True)
    forget_otp = models.CharField(max_length=300, blank=True)
    forget_otp_expiration = models.DateTimeField(blank=True, null=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email.split('@')[0]
