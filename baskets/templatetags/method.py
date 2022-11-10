from django import template
from decimal import Decimal

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
    return num*2

@register.simple_tag(name='real_discount')
def give_me_current_price(product):
    return '%.2f' %(product.price * Decimal(1 - product.category.discount / 100))
