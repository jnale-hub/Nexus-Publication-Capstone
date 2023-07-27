# custom_filters.py

from django import template

register = template.Library()

@register.filter
def ordinalize(value):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return value

    # Convert the number to an ordinal string
    if 10 <= value % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(value % 10, 'th')
    return str(value) + suffix
