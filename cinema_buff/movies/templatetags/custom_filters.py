from django import template

register = template.Library()

@register.filter
def range(value):
    """
    Returns a range of numbers from 0 to value-1
    Usage: {% for i in 5|range %}{{ i }}{% endfor %}
    """
    return range(value)

@register.filter
def add(value, arg):
    """
    Adds two numbers
    Usage: {{ value|add:arg }}
    """
    try:
        return int(value) + int(arg)
    except (ValueError, TypeError):
        return value
