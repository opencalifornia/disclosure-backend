from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^search/', views.search_view),
)
