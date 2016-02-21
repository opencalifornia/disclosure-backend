import importlib
import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import models


def get_disclosure_app_list():
    # Get list of models from apps after those ending in _raw,
    # which should be independent of the main project
    app_list = []
    start_collecting = False
    for app in settings.INSTALLED_APPS:
        if app.endswith('_raw'):  # never collect *_raw
            start_collecting = True
        elif start_collecting:
            app_list.append(app)
    return app_list


def get_mixin_models(app_list=None):
    # Get list of abstract 'mixin' models to exclude;
    # they make the diagram messy.
    mixin_models = []
    for app in (app_list or get_disclosure_app_list()):
        try:
            mod = importlib.import_module(app + '.models')
        except:
            continue
        for obj_name in dir(mod):
            obj = getattr(mod, obj_name)
            try:
                if (issubclass(obj, models.Model) and
                        obj.__name__.endswith('Mixin')):
                    mixin_models.append(obj.__name__)
            except:
                continue
    return mixin_models


class Command(BaseCommand):
    help = 'Generate documentation for models'

    def handle(self, *args, **kwargs):
        self.docs_dir = os.path.join(settings.REPO_DIR, 'docs')

        app_list = get_disclosure_app_list()
        mixin_models = get_mixin_models(app_list)

        # Create the output path
        if not os.path.exists(self.docs_dir):
            os.makedirs(self.docs_dir)

        # Generate the database relationships
        out_file = os.path.join(self.docs_dir, 'model-relationships.png')
        call_command('graph_models', *app_list,
                     group_models=True, inheritance=False,
                     outputfile=out_file,
                     exclude_models=','.join(mixin_models))

        # Generate the inheritance diagram
        out_file = os.path.join(self.docs_dir, 'model-inheritance.png')
        call_command('graph_models', *app_list,
                     group_models=True, inheritance=True,
                     outputfile=out_file,
                     exclude_models=','.join(mixin_models))
