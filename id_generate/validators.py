from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible


def ExactLengthValidator():
    pass
    

def LengthValidator_ORIG(value, length=6):
    if len(str(value)) != length:
        raise ValidationError(f'"{value}" needs to {length} characters!')

