from django import template

from ..models import Basket

register = template.Library()


@register.filter(name='total_quantity')
def total_quantity(value, user):
    return Basket.total_quantity(user)


@register.filter(name='total_sum')
def total_sum(value, user):
    return Basket.total_sum(user)


@register.simple_tag(name='discount')
def bigger_then_you_think(num):
    return num * 2
