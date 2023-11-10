from django import template

register = template.Library()

@register.filter
def zip_lists(a, b, c, d):
    return zip(a, b, c, d)
