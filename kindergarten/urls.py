#coding=utf-8
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from kindergarten.web.views import Index

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kindergarten.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', Index.as_view(), name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^manage/', include("kindergarten.admin.urls")),
    url(r'^api/', include("kindergarten.api.urls")),
    url(r'^ueditor/', include('kindergarten.plugin.Ueditor.urls')),
    url(r'^', include("kindergarten.web.urls")),
)
