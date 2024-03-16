from datetime import datetime

from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def in_the_future(value):
    return value > datetime.now(tz=timezone.get_current_timezone())

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)