from django import template
from herbs.models import *


register = template.Library()

@register.simple_tag()
def get_tovar():
    return Tovar.objects.all()

@register.simple_tag()
def get_group():
    return Group.objects.all()

@register.simple_tag()
def get_sale_cat():
    return Sale_category.objects.all()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    request = context['request'].GET.copy()
    for key, value in kwargs.items():
        request[key] = value
    return request.urlencode()