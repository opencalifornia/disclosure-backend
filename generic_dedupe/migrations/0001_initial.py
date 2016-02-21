# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DedupeLogEntry',
            fields=[
                ('logentry_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='admin.LogEntry')),
                ('class_name', models.CharField(max_length=1024)),
                ('prop_name', models.CharField(max_length=1024)),
                ('true_model_id', models.IntegerField()),
                ('old_true_model_id', models.IntegerField(default=None, null=True, blank=True)),
            ],
            bases=('admin.logentry',),
        ),
    ]
