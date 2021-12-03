from django.db import models


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import RegexValidator
import datetime,calendar

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, mobile, password, **extra_fields):
        """
        Creates and saves a User with the given mobile and password.
        """
        if not mobile:
            raise ValueError('The given email must be set')
        # email = self.normalize_email(email)
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile, password, **extra_fields)

    def create_superuser(self, mobile, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(mobile, password, **extra_fields)

import uuid
class UserProfile(AbstractBaseUser, PermissionsMixin):
    id=models.AutoField(primary_key=True)
    name = models.CharField(_('name'), max_length=50, blank=True)
    mobile = models.CharField(_('mobile'), unique=True, max_length=10, blank=False)
    email = models.EmailField(_('email address'), blank=True)
    password = models.CharField(_('password'),max_length=25,blank=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=False)
    is_admin = models.BooleanField(_('active'), default=False)
    is_manager = models.BooleanField(_('active'), default=False)
    is_tl = models.BooleanField(_('active'), default=False)
    is_agent = models.BooleanField(_('active'), default=False)
    dob=models.DateField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    objects = UserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.name

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


    def __str__(self):
        return self.email

    # def __str__(self):
    #     return str(self.mobile) + ' is sent ' + str(self.otp)


    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }