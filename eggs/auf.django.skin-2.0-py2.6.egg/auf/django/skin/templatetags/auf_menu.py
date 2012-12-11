import re
from django import template

register = template.Library()

@register.simple_tag
def menu_actif(request, pattern, css_class="selected"):
    if re.search(pattern, request.path.strip('/')):
        return css_class
    else:
        return ''

