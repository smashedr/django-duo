import logging
from django import template

logger = logging.getLogger('app')
register = template.Library()


@register.filter(name='round_it')
def round_it(value, decimal=2):
    if decimal == 0:
        return int(float(value))
    return round(float(value), decimal)
