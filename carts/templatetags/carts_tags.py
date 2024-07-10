from django import template
from carts.utils import get_user_carts
from orders.models import LandsUndNumbers

register = template.Library()

@register.simple_tag()
def user_carts(request):
    return get_user_carts(request)

@register.simple_tag()
def get_land_and_number():
    return LandsUndNumbers.objects.all()