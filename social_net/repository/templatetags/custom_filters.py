import os.path

from django import template

register = template.Library()

@register.filter
def split_by_slash(value):
    result = str(value).split(os.path.sep)
    return [(result[i], os.path.join(*result[:i + 1])) for i in range(len(result))]