import csv

from ...models import City, State
from .dump_aliases import Command as DumpCommand


class Command(DumpCommand):
    help = 'Load aliases to models'

    def handle(self, *args, **options):
        self.load_aliases(cls=City, filename=options['filename'])

    def load_aliases(self, cls, filename):
        with open(filename, 'r') as fp:
            reader = csv.DictReader(fp, fieldnames=self.FIELD_NAMES)
            reader.next()  # skip header row

            for row in reader:
                # Get/create the state (if set)
                if row['state__short_name']:
                    state, _ = State.objects.get_or_create(
                        short_name=row['state__short_name'])
                else:
                    state = None

                # Get/create the city
                city, _ = City.objects.get_or_create(
                    name=row['name'], state=state)

                if row['name'] == 'name':
                    # header row
                    continue

                elif city.aliases:
                    if city.aliases != row['aliases']:
                        # Look for potential conflicts
                        print("WARNING: skipping conflicting aliases; "
                              "current (%s) vs. loaded (%s)" % (
                                  city.aliases, row['aliases']))
                    continue

                # Report results
                print("Setting aliases for %s to %s" % (
                    row['name'], row['aliases']))
                city.aliases = row['aliases']
                city.save()
