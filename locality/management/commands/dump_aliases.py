import csv

from django.core.management.base import BaseCommand

from ...models import City


class Command(BaseCommand):
    help = 'Dump aliases for cities'

    FIELD_NAMES = ['name', 'short_name', 'state__short_name', 'aliases']
    CSV_FILE = 'aliases.csv'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('filename', nargs='?', default=self.CSV_FILE)

    def handle(self, *args, **options):
        self.dump_aliases(cls=City, filename=options['filename'])

    def dump_aliases(self, cls, filename):
        queryset = cls.objects.exclude(
            aliases__isnull=True).exclude(aliases__exact='')
        values = queryset.values(*self.FIELD_NAMES)

        with open(filename, 'w') as fp:
            writer = csv.DictWriter(fp, fieldnames=self.FIELD_NAMES)
            writer.writeheader()
            for row in values:
                writer.writerow(row)
