from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_raw.models.base import CalAccessBaseModel


@python_2_unicode_compatible
class FipsEntity(CalAccessBaseModel):
    """
    Entities that have FIPS IDs (state/county/city)
    """
    TYPE_STATE = 'ST'
    TYPE_COUNTY = 'CO'
    TYPE_CITY = 'CI'
    TYPES = (
        (TYPE_STATE, 'state'),
        (TYPE_COUNTY, 'county'),
        (TYPE_CITY, 'city'),
    )
    fips_id = models.IntegerField(
        db_column='fips_id',
        primary_key=True
    )
    name = models.CharField(
        max_length=1024,
        db_column='name'
    )
    type = models.CharField(
        max_length=2,
        db_column='type',
        choices=TYPES
    )

    class Meta:
        app_label = 'fips'
        db_table = 'fips'
        verbose_name = 'FIPS_ENTITY'
        verbose_name_plural = 'FIPS_ENTITIES'

    def __str__(self):
        return "%s of %s (%d)" % (self.type, self.name, self.fips_id)
