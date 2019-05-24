from django import template
from django.utils.termcolors import colorize as dj_colorize

register = template.Library()


@register.filter
def colorize(value, fg):
    return dj_colorize(value, tuple(), fg=fg)
