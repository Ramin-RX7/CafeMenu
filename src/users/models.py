from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class UserManager(BaseUserManager):
    def create_user(self, phone, password, **other_fields):
        if phone is None:
            raise ValueError("Phone not given")

        user = self.model(phone=phone, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

# Create your models here.
