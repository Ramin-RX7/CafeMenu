from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)

from core.models import BaseModel
from core.validators import phone_validator
from .managers import UserManager, ClientManager
from .fields import PhoneNumberField


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    phone = PhoneNumberField(validators=[phone_validator], unique=True, max_length=20)

    first_name = models.CharField(max_length=50, blank=True, default="")
    last_name = models.CharField(max_length=50, blank=True, default="")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.phone}"


class Staff(User):
    class Meta:
        proxy = True


class Client(User):
    objects = ClientManager()
    class Meta:
        proxy = True
