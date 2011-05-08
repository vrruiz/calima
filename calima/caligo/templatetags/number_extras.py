from django import template

register = template.Library()

@register.filter
def dotpoint(value):
    return str(value).replace(',', '.')
