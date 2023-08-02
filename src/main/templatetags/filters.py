from django import template

register = template.Library()

@register.filter
def mul(value, other):
    return value*other
