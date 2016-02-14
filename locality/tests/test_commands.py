import csv
import os.path as op
import tempfile

from django.core.management import call_command
from django.test import TestCase

from locality.models import City


class DumpLoadEmptyTest(TestCase):
    """Unit tests on generic methods within the command file."""
    verbosity = 0

    def test_empty_with_file(self):
        _, filename = tempfile.mkstemp()

        call_command('dump_aliases', filename, verbosity=self.verbosity)
        self.assertTrue(op.exists(filename))

        # Empty file
        with open(filename, 'r') as fp:
            reader = csv.DictReader(fp)
            self.assertRaises(StopIteration, reader.next)

        # Smoke test for reading an empty file
        call_command('load_aliases', filename, verbosity=self.verbosity)


class DumpLoadEmptyTestWithVerbosity(DumpLoadEmptyTest):
    """Redo DumpLoadEmptyTest with verbosity=1"""
    verbosity = 1


class LoadFixtureTest(TestCase):
    """Unit tests on generic methods within the command file."""
    verbosity = 0

    def test_load_current_data(self):
        City.objects.all().delete()
        self.assertEqual(City.objects.all().count(), 0)

        call_command('load_aliases', verbosity=self.verbosity)
        self.assertNotEqual(City.objects.all().count(), 0)

        for city in City.objects.all():
            self.assertNotEqual(city.aliases, None, city.name)
            self.assertNotEqual(city.aliases, '', city.name)

    def test_load_conflict_data(self):
        City.objects.all().delete()
        self.assertEqual(City.objects.all().count(), 0)

        call_command('load_aliases', verbosity=self.verbosity)
        self.assertNotEqual(City.objects.all().count(), 0)

        # Introduce a change/conflict.
        for city in City.objects.all():
            city.aliases = 'stuff'
            city.save()

        call_command('load_aliases', verbosity=self.verbosity)

        # Make sure each has been merged.
        for city in City.objects.all():
            self.assertIn('stuff', city.aliases.split(','),
                          "Don't lose old aliases on load")
            self.assertNotEqual('stuff', city.aliases,
                                "Don't lose new aliases on load")

    def test_load_twice(self):
        City.objects.all().delete()
        self.assertEqual(City.objects.all().count(), 0)

        call_command('load_aliases', verbosity=self.verbosity)
        n_cities = City.objects.all().count()
        self.assertNotEqual(n_cities, 0)

        call_command('load_aliases', verbosity=self.verbosity)
        self.assertEqual(City.objects.all().count(), n_cities,
                         "Loading a 2nd time shouldn't change the # of ciites")


class LoadFixtureTestWithVerbosity(LoadFixtureTest):
    """Redo DumpLoadEmptyTest with verbosity=1"""
    verbosity = 1
