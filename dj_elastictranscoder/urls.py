try:
    from django.conf.urls import url, patterns
except ImportError:
    from django.conf.urls.defaults import url, patterns  # Support for Django < 1.4

urlpatterns = patterns('dj_elastictranscoder.views',
    url(r'^endpoint/$', 'endpoint'),
)
