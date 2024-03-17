from django.db import models
from django.core.exceptions import ValidationError

from core.validators import phone_validator



class PhoneNumberField(models.CharField):
    def get_prep_value(self, value):
        if value is None:
            return value

        try:
            regex = phone_validator(value)
        except ValidationError as e:
            raise e

        phone_parts = regex.groupdict()
        phone =  phone_parts["operator"] + phone_parts["middle3"] + phone_parts["last4"]
        return phone
