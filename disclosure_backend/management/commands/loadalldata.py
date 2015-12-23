import glob
import os
from django.conf import settings
from django.core.management import call_command
from calaccess_raw.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    help = 'Generate documentation for raw CAL-ACCESS database models'

    def handle(self, *args, **kwargs):
        for app in settings.INSTALLED_APPS:
            try:
                app_mod = __import__(app)
            except:
                continue
            app_path = os.path.dirname(app_mod.__file__)
            fixture_path = os.path.join(app_path, 'fixtures')
            for json_file in glob.glob(os.path.join(fixture_path, '*.json')):
                print("Loading fixture for %s from %s" % (app, fixture_path))
                call_command('loaddata', json_file)
