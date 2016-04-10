from unidecode import unidecode

from django.template import defaultfilters


# http://www.djangosnippets.org/snippets/342/

def preload_templatetags():

    from django.conf import settings

    #from django.template.loader import add_to_builtins

    from django.template.base import add_to_builtins
    import django.template.loader

    try:
        for lib in settings.TEMPLATE_TAGS:
            add_to_builtins(lib)
    except AttributeError:
        pass

def slugify(value):
    return defaultfilters.slugify(
        unidecode(
            value
        )
    )
