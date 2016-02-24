from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Basic django views
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
        'show_indexes': True}),

    # Non-API views
    url(r'^$', views.homepage_view),
    url(r'^missing-data/$', views.missing_data_view),

    # inclusions
    url(r'', include('ballot.urls')),
    url(r'', include('election_day.urls')),
    url(r'', include('finance.urls')),
    url(r'', include('locality.urls')),  # empty

    # API views
    url(r'^docs/', include('rest_framework_swagger.urls')),

    url(r'^locality/search/', views.search_view,
        name='search'),

    url(r'^ballot/(?P<ballot_id>[0-9]+)/disclosure_summary$',
        views.locality_disclosure_summary_view,
        name='locality_disclosure_summary'),

    url(r'referendum/(?P<referendum_id>[0-9]+)/supporting$',
        views.ReferendumViewSet.as_view(actions={'get': 'supporting'}),
        name='referendum_supporting'),
    url(r'referendum/(?P<referendum_id>[0-9]+)/opposing$',
        views.ReferendumViewSet.as_view(actions={'get': 'opposing'}),
        name='referendum_opposing'),

    url(r'candidate/(?P<candidate_id>[0-9]+)/supporting',
        views.CandidateViewSet.as_view(actions={'get': 'supporting'}),
        name='candidate_supporting'),
    url(r'candidate/(?P<candidate_id>[0-9]+)/opposing$',
        views.CandidateViewSet.as_view(actions={'get': 'opposing'}),
        name='candidate_opposing'))

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
