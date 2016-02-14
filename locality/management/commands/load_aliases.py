import csv

from ...models import City, State
from .dump_aliases import Command as DumpCommand


class Command(DumpCommand):
    help = 'Load aliases to models'

    def handle(self, *args, **options):
        self.load_aliases(cls=City, filename=options['filename'],
                          verbosity=options['verbosity'])

    def load_aliases(self, cls, filename, verbosity=1):
        with open(filename, 'r') as fp:
            reader = csv.DictReader(fp, fieldnames=self.FIELD_NAMES)

            for ri, row in enumerate(reader):
                if ri == 0 and row['name'] == 'name':
                    continue  # Header row, skip

                # Get/create the state (if set)
                state, _ = State.objects.get_or_create(
                    short_name=row['state__short_name'])

                # Get/create the city
                city, _ = City.objects.get_or_create(
                    name=row['name'], state=state)

                if row['name'] == 'name':
                    # header row
                    continue

                elif city.aliases and city.aliases != row['aliases']:
                    # Merge aliases
                    all_aliases = '%s,%s' % (city.aliases, row['aliases'])
                    unique_aliases = set(all_aliases.split(','))
                    merged_aliases = ','.join(sorted(unique_aliases))
                    if verbosity:
                        print("Merged %s + %s to %s" % (
                            row['aliases'], city.aliases, merged_aliases))
                    row['aliases'] = merged_aliases

                # Make change, report results
                city.aliases = row['aliases']
                city.save()
                if verbosity:
                    print("Set aliases for %s to %s" % (
                        row['name'], row['aliases']))
