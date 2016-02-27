from django.contrib import admin

from .forms import DedupeForm
from . import models

admin.site.register(models.DedupeLogEntry)


class DedupeAdmin(admin.ModelAdmin):
    """Adds a dropdown for selecting the 'true model'."""
    form = DedupeForm

    class Meta:
        fields = '__all__'
