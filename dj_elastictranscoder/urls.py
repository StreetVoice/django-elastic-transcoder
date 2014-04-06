from django.conf.urls import url, patterns

urlpatterns = patterns('dj_elastictranscoder.views',
    url(r'^sns_endpoint/$', 'sns_endpoint'),
)
