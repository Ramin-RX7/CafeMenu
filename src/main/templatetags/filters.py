from django import template

register = template.Library()

@register.filter
def mul(value, other):
    return float(value)*float(other)
