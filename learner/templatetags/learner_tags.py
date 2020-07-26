from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()
@register.filter(name='fix_val')
def fix_val(value):
    return value.replace(' ','-')

@register.filter(name='get_type')
def get_type(value):
    y=1 if (type(value)==list) else 0    
    return y
