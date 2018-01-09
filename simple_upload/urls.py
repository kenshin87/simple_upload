from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^$', views.index, name='upload_index'),
    url(r'^upload/$', views.upload, name='upload_upload'),
]
