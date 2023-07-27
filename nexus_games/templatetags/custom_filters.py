from django import template

register = template.Library()

@register.filter(name='ordinalize')
def ordinalize(value):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return value

    if 10 <= value % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(value % 10, 'th')
    return str(value) + suffix
