from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_setting_or_raise(setting_name):
    try:
        value = getattr(settings, setting_name)
    except AttributeError:
        raise ImproperlyConfigured('Please provide {0}'.format(setting_name))
    return value
