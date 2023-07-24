from django.db import models

class Category(models.Model):
    title = models.CharFields(max_length=30)
    description = models.TextFields(blank=True, null=True)

    def __str__(self) -> str:
        return self.title