import importlib
import operator
from django.utils.html import format_html


def tuple_index_elements(theset, elemnum=1):
    """gets tuple of each element(default=1)
        within nested list/tuple/etc of lists/tuples
    """
    get = operator.getitem
    return tuple([get(get(theset,each),elemnum)
            for each in range(theset.__len__())])


def admin_changelist_link(
    attr,
    short_description,
    empty_description="-",
    query_string=None
):
    """Decorator used for rendering a link to the list display of
    a related model in the admin detail page.

    attr (str):
        Name of the related field.
    short_description (str):
        Field display name.
    empty_description (str):
        Value to display if the related field is None.
    query_string (function):
        Optional callback for adding a query string to the link.
        Receives the object and should return a query string.

    The wrapped method receives the related object and
    should return the link text.

    Usage:
        @admin_changelist_link('credit_card', _('Credit Card'))
        def credit_card_link(self, credit_card):
            return credit_card.name

    Decorator code found on https://medium.com/@hakibenita/things-you-must-know-about-django-admin-as-your-app-gets-bigger-6be0b0ee9614 in section "admin_changelist_link"
    """
    def wrap(func):
        def field_func(self, obj):
            related_obj = getattr(obj, attr)
            if related_obj is None:
                return empty_description
            url = ""
            if query_string:
                url += '?' + query_string(obj)
            return format_html(
                '<a href="{}">{}</a>',
                url,
                func(self, related_obj)
            )
        field_func.short_description = short_description
        field_func.allow_tags = True
        field_func.admin_order_field = attr
        return field_func
    return wrap


def field_is_empty(field):
    """check for empty field value, post str.strip"""
    #FIXME: field_is_empty not valid response on field bool=True !
    if field \
          and str(field) != '' \
          and str(field).strip() != '' :
        empty = False
    else:
        empty = True
    return empty


# def get_required_fields(model_meta):
#     """subset of get_fields where blank == False"""
#     fields - model_meta.get_fields()
#     reqd_fields = [f for f in fields
#             if hasattr(f, 'blank') and f.blank == False]
#     return reqd_fields

