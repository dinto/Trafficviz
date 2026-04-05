import json
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='jsonify')
def jsonify(value):
    """Convert a Python object to a JSON string safe for use in HTML attributes."""
    return mark_safe(json.dumps(value))
