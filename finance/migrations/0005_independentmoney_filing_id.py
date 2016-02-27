# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_auto_20160227_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='independentmoney',
            name='filing_id',
            field=models.CharField(default=None, max_length=32, null=True, help_text='Transaction ID (specific to government processing entity)', blank=True),
        ),
    ]
