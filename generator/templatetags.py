from django import template

register = template.Library()

# from: https://stackoverflow.com/a/42859395/1600630
@register.filter
def pdb(element):
    from django.conf import settings
    if settings.DEBUG:
        import pdb
        pdb.set_trace()
    return element

