# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='independentmoney',
            name='cumulative_amount',
            field=models.FloatField(default=None, help_text='Total monetary value of provided benefits, to date of this transaction.', null=True, blank=True),
        ),
    ]
