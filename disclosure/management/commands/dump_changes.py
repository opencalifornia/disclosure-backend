import os.path as op

from django.core import serializers
from django.core.management.base import BaseCommand
from django.contrib.admin.models import LogEntry

from disclosure import fixtures


def model_and_parents(model):
    """Get a model and all parents.

    This helps overcome the limits of Django serialization for
    multi-table inheritance, where only the "local fields" on an
    object are serialized.
    """
    rv = []
    if model:
        rv.append(model)
        for cls in model._meta.get_parent_list():
            rv.append(cls.objects.get(id=model.id))
    return rv


class Command(BaseCommand):
    help = 'Serialize all models edited through the admin interface.'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('filename', default=self.FIXTURE_FILE)

    FIXTURE_FILE = op.join(op.dirname(fixtures.__file__),
                           'admin-edited-models.json')

    def handle(self, *args, **options):
        models = []
        for entry in LogEntry.objects.all():
            edited_object = entry.get_edited_object()

            # Add the object and parents
            models += model_and_parents(edited_object)

        # Dump to output.
        with open(options['filename'], 'w') as fp:
            fp.write(serializers.serialize("json", models))
