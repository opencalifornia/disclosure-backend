from rest_framework.routers import SimpleRouter
# from django.conf.urls import patterns, url
from django.contrib import admin

from ..views import ballot as views

admin.autodiscover()

api = SimpleRouter()
api.register(r'locality/(?P<locality_id>[0-9]+)', views.BallotViewSet,
             base_name='ballot')
urlpatterns = api.urls
