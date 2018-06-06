from django import template
from django.conf import settings

register = template.Library()

# modified orig from https://stackoverflow.com/a/21593607/1600630
@register.simple_tag
def settings_value(name):
    return str(getattr(settings, name, ""))

