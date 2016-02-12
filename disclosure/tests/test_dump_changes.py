import os.path as op
import json
import tempfile
import time

from django.core.management import call_command
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from django.test import TestCase

from disclosure.management.commands.dump_changes import Command
from finance.tests.test_xformnetfilerawdata import WithForm460ADataTest
from locality.models import City


class DumpChangesEmptyTest(TestCase):
    """Unit tests on generic methods within the command file."""

    def test_empty_with_file(self):
        _, filename = tempfile.mkstemp()

        call_command('dump_changes', filename)
        self.assertTrue(op.exists(filename))

        with open(filename, 'r') as fp:
            data = json.load(fp)
        self.assertEqual(len(data), 0)

        # Smoke test
        call_command('loaddata', filename)


class DumpChangesLoadTest(TestCase):
    """Unit tests on generic methods within the command file."""

    def test_load_current_data(self):
        self.assertEqual(City.objects.all().count(), 0)
        call_command('loaddata', Command.FIXTURE_FILE)
        self.assertNotEqual(City.objects.all().count(), 0)


class DumpChangesWithDataTest(WithForm460ADataTest, TestCase):
    """
    action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id
    """
    @classmethod
    def setUpClass(cls):
        WithForm460ADataTest.setUpClass()
        TestCase.setUpClass()
        User.objects.create_superuser(
            username='admin', password='admin', email='')

    def test_dump_a_change(self):

        # Change the city
        city = City.objects.all()[0]
        old_name = city.name
        new_name = "The city build on rock 'n roll"
        city.name = new_name
        city.save()

        # Store the log
        logentry = LogEntry(object_id=city.id, object_repr=str(city),
                            action_flag=2, change_message="Hi!",
                            content_type_id=88,
                            user_id=User.objects.all()[0].id)
        logentry.save()

        # Dump the changes
        _, filename = tempfile.mkstemp()
        call_command('dump_changes', filename)
        self.assertTrue(op.exists(filename))

        # Load the changes
        city_id = city.id
        city.delete()
        del city
        call_command('loaddata', filename)

        # Verify the loaded data
        new_city = City.objects.get(id=city_id)
        self.assertEqual(new_city.name, "The city build on rock 'n roll")
