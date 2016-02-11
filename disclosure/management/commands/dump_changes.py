from django.core import serializers
from django.core.management.base import BaseCommand
from django.contrib.admin.models import LogEntry

from locality.models import Locality


class Command(BaseCommand):
    help = 'Generate documentation for models'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('filename', default=self.FIXTURE_FILE)

    def handle(self, *args, **options):
        models = []
        for entry in LogEntry.objects.all():
            edited_object = entry.get_edited_object()
            if edited_object is None:
                continue

            # Add the object
            models.append(edited_object)

            # Add the locality info
            if issubclass(edited_object.__class__, Locality):
                models.append(Locality.objects.get(id=edited_object.id))

        # Dump to output.
        with open(options['filename'], 'w') as fp:
            fp.write(serializers.serialize("json", models))
