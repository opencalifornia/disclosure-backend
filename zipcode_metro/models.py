from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_raw.models.base import CalAccessBaseModel

@python_2_unicode_compatible
class ZipCodeMetro(CalAccessBaseModel):
    """
    A Static set of ZIP code to "metro" name mappings.
    """
    zip_code = models.IntegerField(
        db_column='ZipCode'
    )
    state_name = models.CharField(
        max_length=1024,
        db_column='StateName'
    )
    county_name = models.CharField(
        max_length=1024,
        db_column='CountyName'
    )
    city_name = models.CharField(
        max_length=1024,
        db_column='CityName'
    )
    psa_code = models.IntegerField(
        db_column='PSACode'
    )
    psa_title = models.CharField(
        max_length=1024,
        db_column='PSATitle'
    )

    class Meta:
        app_label = 'zipcode_metro'
        db_table = 'ZIPCODE_METRO'
        verbose_name = 'ZIPCODE_METRO'
        verbose_name_plural = 'ZIPCODE_METRO'

    def __str__(self):
        return "%d: %s" % (self.zip_code, self.city_name)

