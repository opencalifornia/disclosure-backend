from django.core import serializers
from django.core.management.base import BaseCommand

from ...models import City, County, Locality


class Command(BaseCommand):
    help = 'Generate documentation for models'

    def handle(self, *args, **kwargs):
        queryset = []
        for cls in [Locality, City, County]:
            queryset += cls.objects.exclude(aliases__isnull=True).exclude(aliases__exact='')

        filename = args[0] if args else 'aliases.json'
        with open(filename, 'w') as fp:
            fp.write(serializers.serialize("json", queryset))
