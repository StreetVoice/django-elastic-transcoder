try:
    from django.conf.urls import url, patterns
except ImportError:
    from django.conf.urls.defaults import url, patterns  # Support for Django < 1.4

urlpatterns = patterns(
    'dj_elastictranscoder.views',
    url(r'^endpoint/$', 'aws_endpoint'),
    url(r'^aws_endpoint/$', 'aws_endpoint', name='aws_endpoint'),
    url(r'^qiniu_endpoint/$', 'qiniu_endpoint', name='qiniu_endpoint'),
    url(r'^aliyun_endpoint', 'aliyun_endpoint', name='aliyun_endpoint'),
)
