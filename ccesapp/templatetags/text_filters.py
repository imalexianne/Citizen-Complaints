import re
from django import template

register = template.Library()

@register.filter
def remove_parentheses(value):
    value = str(value)  # Convert to string first
    return re.sub(r'\(.*?\)', '', value)  # Remove anything inside parentheses
