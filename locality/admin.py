from django.contrib import admin

from . import models
from generic_dedupe.admin import DedupeAdmin


admin.site.register(models.City, DedupeAdmin)
admin.site.register(models.County)
admin.site.register(models.State)
admin.site.register(models.ZipCode)
