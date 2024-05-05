from django import template
import random
from dashboard.models import Category

register = template.Library()

@register.simple_tag
def random_sample(sequence, count):
    return random.sample(sequence, count)

@register.simple_tag
def get_categories():
    return Category.objects.all()

@register.filter
def to_float(value):
    try:
        float_value = float(value)
        return "{:.2f}".format(float_value)
    except (ValueError, TypeError):
        return ""
    
@register.simple_tag
def multiply(value1, value2):
    return value1 * value2