from django.conf.urls import url
from dj_elastictranscoder import views

urlpatterns = [
    url(r'^endpoint/$', views.aws_endpoint),
    url(r'^aws_endpoint/$', views.aws_endpoint, name='aws_endpoint'),
    url(r'^qiniu_endpoint/$', views.qiniu_endpoint, name='qiniu_endpoint'),
    url(r'^aliyun_endpoint', views.aliyun_endpoint, name='aliyun_endpoint'),
]
