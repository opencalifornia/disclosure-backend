from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django.views.static.serve', {
        'path': 'index.html',
        'document_root': settings.STATIC_ROOT,
    }),
    url(r'^(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
        'show_indexes': True,
    }),
)
