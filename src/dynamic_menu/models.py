from django.db import models

from main.models import BaseModel,SingletonModel



class MainInfo(BaseModel,SingletonModel):
    title = models.CharField(max_length=25)
    motto = models.CharField(max_length=20,blank=True)
    short_description = models.CharField(max_length=150, blank=True)
    about_us = models.TextField(blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True,null=True)
    logo = models.ImageField(upload_to='images/dynamic_menu/',)
    icon = models.ImageField(upload_to='images/dynamic_menu/')

    def __str__(self) -> str:
        return "Main Info"
