from django.db import models
from django.core.exceptions import ValidationError



class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if type(self).objects.exists():
            existing_instance = type(self).objects.first()
            if self.pk != existing_instance.pk:
                raise ValidationError("Only updates to the existing instance are allowed.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass
