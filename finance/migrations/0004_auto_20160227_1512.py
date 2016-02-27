# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='independentmoney',
            name='reporting_period',
            field=models.ForeignKey(verbose_name='Form & Reporting Period', to='finance.ReportingPeriod', help_text='Form + date range'),
        ),
    ]
