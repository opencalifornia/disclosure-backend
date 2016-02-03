from django.contrib import admin

from rest_framework.routers import SimpleRouter

from . import views


admin.autodiscover()

api = SimpleRouter()
api.register(r'money', views.IndependentMoneyViewSet)
api.register(r'committee', views.CommitteeViewSet)
urlpatterns = api.urls
