from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from rest_framework.routers import SimpleRouter

from . import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.homepage_view),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
        'show_indexes': True}),

    url(r'', include('ballot.urls')),
    url(r'', include('election_day.urls')),
    url(r'', include('finance.urls')),
    # url(r'', include('locality.urls')),  # empty
    url(r'^docs/', include('rest_framework_swagger.urls')),

    url(r'^search/', views.search_view,
        name='search'),

    # Details for specific objects
    url(r'^locations/(?P<locality_id>[0-9]+)$', views.location_view,
        name='locality_detail'))

api = SimpleRouter()
api.register(r'locality/(?P<locality_id>[0-9]+)', views.LocalityViewSet,
             base_name='locality')
urlpatterns += api.urls
