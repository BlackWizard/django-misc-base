# coding=utf-8

from django import template

from django.utils.safestring import mark_safe

register = template.Library()


import logging
log = logging.getLogger(__name__)


@register.simple_tag
def clfix():
    return mark_safe('<div class="clearfix"><!-- --></div>')

@register.filter(name='concat')
def concat(val, arg):
    return "%s%s" % (val, arg)

@register.filter
def subtract(val, arg):
    return val - arg

@register.filter
def limit(qs, n):
    try:
        if isinstance(qs, (list, tuple)):
            return qs[:n]
        else:
            return qs.all()[:n]
    except:
        return qs

def active_filter(qs):
    return qs.filter(status=0)

@register.filter
def rupluralize(value, arg="балл,балла,баллов"):
    args = arg.split(",")
    if not value:
        return "%s %s" % (value, args[2])
    number = abs(int(value))
    a = number % 10
    b = number % 100
    if (a == 1) and (b != 11):
        return "%s %s" % (value, args[0])
    elif (a > 1) and (a < 5) and ((b < 10) or (b > 20)):
        return "%s %s" % (value, args[1])
    else:
        return "%s %s" % (value, args[2])
