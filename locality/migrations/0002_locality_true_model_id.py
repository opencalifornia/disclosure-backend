# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locality', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='locality',
            name='true_model_id',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
    ]
