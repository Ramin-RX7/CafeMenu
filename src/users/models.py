from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator



class UserManager(BaseUserManager):

    def create_user(self, phone, password, **other_fields):
        if phone is None:
            raise ValueError("Phone not given")

        user = self.model(phone=phone, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, phone, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superusermust have is_superuser=True.')

        return self.create_user(phone, password, **other_fields)



class User(AbstractBaseUser, PermissionsMixin):
    phone_validator = RegexValidator(r"(((+|00)(98))|0)9\d{2}-?\d{3}-?\d{4}")
    phone = models.CharField(validators=[phone_validator], unique=True, max_length=20)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.phone}"