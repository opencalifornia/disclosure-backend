# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FipsEntity',
            fields=[
                ('fips_id', models.IntegerField(serialize=False, primary_key=True, db_column='fips_id')),
                ('name', models.CharField(max_length=1024, db_column='name')),
                ('type', models.CharField(max_length=2, db_column='type', choices=[('ST', 'state'), ('CO', 'county'), ('CI', 'city')])),
            ],
            options={
                'db_table': 'fips',
                'verbose_name': 'FIPS_ENTITY',
                'verbose_name_plural': 'FIPS_ENTITIES',
            },
        ),
    ]
