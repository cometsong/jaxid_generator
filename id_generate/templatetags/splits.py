from django import template

register = template.Library()

# modified orig from https://stackoverflow.com/q/8317537/1600630
@register.filter(name='split')
def split(value, arg):
    return value.split(arg)
