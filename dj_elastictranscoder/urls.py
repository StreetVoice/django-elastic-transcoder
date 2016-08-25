import django

from dj_elastictranscoder.views import endpoint as transcoder_endpoint

try:
    from django.conf.urls import url, patterns
except ImportError:
    try:
        from django.conf.urls.defaults import url, patterns  # Support for Django < 1.4
    except ImportError:
        from django.conf.urls import url

if django.VERSION[0] >= 1 and django.VERSION[1] >= 10:
    urlpatterns = (url(r'^endpoint/$', transcoder_endpoint, name='transcoder_endpoint'),)
else:
    urlpatterns = patterns('dj_elastictranscoder.views',
        url(r'^endpoint/$', 'endpoint'),
    )
