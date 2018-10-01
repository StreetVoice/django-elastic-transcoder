import django


if django.get_version() >= '1.9':
    from django.conf.urls import url
    from dj_elastictranscoder import views

    urlpatterns = [
        url(r'^endpoint/$', views.aws_endpoint),
        url(r'^aws_endpoint/$', views.aws_endpoint, name='aws_endpoint'),
        url(r'^qiniu_endpoint/$', views.qiniu_endpoint, name='qiniu_endpoint'),
        url(r'^aliyun_endpoint', views.aliyun_endpoint, name='aliyun_endpoint'),
    ]

else:
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
