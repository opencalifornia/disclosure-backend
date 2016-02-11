import numpy as np

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db import models
from django.db.models.fields.related import OneToOneRel
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible


class ReverseLookupStringMixin(object):
    def reverse_lookup(self):
        for relationship in self._meta.related_objects:
            attr = relationship.name
            if (isinstance(relationship, OneToOneRel) and hasattr(self, attr)):
                return getattr(self, attr)
        return None

    def type(self):
        obj = self.reverse_lookup()
        return obj.__class__.__name__.lower() if obj else None

    def __str__(self):
        obj = self.reverse_lookup()
        return unicode(obj) if obj else ''


class LocalityQuerySet(models.QuerySet):
    def get(self, *args, **kwargs):
        if np.any([key.startswith('name__') for key in kwargs]):
            raise NotImplementedError("name__ attributes.")

        try:
            return super(LocalityQuerySet, self).get(*args, **kwargs)
        except ObjectDoesNotExist as odne:
            # Already did our best; stick with the exception.
            if 'name' not in kwargs or np.any([key.startswith('aliases') in kwargs]):
                raise

        # Try augmented search
        name = kwargs.pop('name')
        query = models.Q(aliases__contains=',%s,' % name)
        query |= models.Q(aliases__startswith='%s,' % name)
        query |= models.Q(aliases__endswith=',%s' % name)
        args += (query,)
        try:
            return super(LocalityQuerySet, self).get(*args, **kwargs)
        except MultipleObjectsReturned:
            raise odne  # go with original error; clearer to users.


class LocalityAliasManager(models.Manager):
    def get_queryset(self):
        return LocalityQuerySet(self.model, using=self._db)


@python_2_unicode_compatible
class Locality(models.Model, ReverseLookupStringMixin):
    """
    A base table that gives a globally unique ID to any
    location (city, state, etc)
    """
    name = models.CharField(max_length=128, blank=True, null=True, default=None)
    short_name = models.CharField(max_length=32, blank=True, null=True, default=None)
    aliases = models.CharField(max_length=4096, blank=True, null=True, default=None,
                               help_text="Comma-separated list of alternate spellings for `name`")

    objects = models.Manager()
    aliased_objects = LocalityAliasManager()

    @classmethod
    def name_is_aliased(cls, name):
        if name is None:
            return False
        for model in cls.objects.filter(aliases__contains=name):
            if name in model.aliases.split(','):
                return True
        return False

    def clean(self):
        """Make aliases unique & clean."""
        if self.aliases is not None:
            aliases_set = set([a.strip()
                               for a in self.aliases.strip().split(',')])
            aliases_cleaned = ','.join(aliases_set)
            self.aliases = aliases_cleaned or None  # convert blank to None
        return super(Locality, self).clean()

    def save(self, *args, **kwargs):
        self.clean()
        if self.name_is_aliased(self.name):
            raise Exception('No fair saving an aliased name!')
        super(Locality, self).save(*args, **kwargs)

    def __str__(self):
        return (ReverseLookupStringMixin.__str__(self) or
                self.name or self.short_name or str(self.id))

    class Meta:
        verbose_name_plural = 'localities'
        ordering = ('name', 'short_name')


class FipsMixin(Locality):
    """
    Abstract class, for any model that has a fips_id
    """
    fips_id = models.IntegerField(blank=True, null=True, default=None)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class City(FipsMixin):
    """
    City
    """
    county = models.ForeignKey('County', blank=True, null=True, default=None)
    state = models.ForeignKey('State')

    objects = models.Manager()
    aliased_objects = LocalityAliasManager()

    def __str__(self):
        return '%s, %s' % (self.name or self.short_name, self.state)

    class Meta:
        verbose_name_plural = 'cities'
        ordering = ('state__short_name', 'county', 'name', 'short_name')


@python_2_unicode_compatible
class County(FipsMixin):
    """
    County
    """
    state = models.ForeignKey('State')

    objects = models.Manager()
    aliased_objects = LocalityAliasManager()

    def __str__(self):
        # See https://code.djangoproject.com/ticket/25218 on why __unicode__
        return '%s, %s' % (Locality.__unicode__(self), self.state)

    class Meta:
        verbose_name_plural = 'counties'
        ordering = ('state__short_name', 'name', 'short_name')


@python_2_unicode_compatible
class State(FipsMixin):
    """
    State
    """
    # Uses short_name, so don't use the alias manager.

    def __str__(self):
        return self.short_name or self.name

    class Meta:
        ordering = ('short_name', 'name')


@python_2_unicode_compatible
class ZipCode(Locality):
    """
    A Static set of ZIP code to "metro" name mappings.
    """
    city = models.ForeignKey('City', blank=True, null=True, default=None)
    county = models.ForeignKey('County', blank=True, null=True, default=None)
    state = models.ForeignKey('State', blank=True, null=True, default=None)
    # Uses short_name, so don't use the alias manager.

    def __str__(self):
        return self.short_name or self.name


@receiver(post_save, sender=Locality)
@receiver(post_save, sender=City)
@receiver(post_save, sender=County)
def update_city_aliases(sender, instance, **kwargs):
    if instance.aliases:
        current_aliases = []
        new_aliases = [a.strip() for a in instance.aliases.split(',')]
        if len(new_aliases) == 0:
            remote_models = []
        else:
            remote_models = [obj
                             for a in new_aliases
                             for obj in sender.objects.filter(name__iexact=a)]
            if len(remote_models) == 1 and remote_models[0].aliases:
                # Remote model already has aliases, so flip things:
                # Call that the instance, and make the instance
                #   one of the remote models
                new_aliases = [instance.name]
                instance, remote_models = remote_models[0], [instance]
                current_aliases = [a.strip() for a in instance.aliases.split(',')]

        # Normalize aliases
        all_aliases = current_aliases + new_aliases
        all_aliases_text = ','.join(all_aliases)
        if instance.aliases != all_aliases_text:
            instance.aliases = all_aliases_text
            instance.save()

        # Migrate any foreign keys off of aliases, then delete.
        for model in remote_models:
            for relationship in model._meta.related_objects:
                attr = relationship.name
                if hasattr(model, attr):
                    for obj in getattr(model, attr).get_queryset():
                        setattr(obj, relationship.field.name, instance)
            model.delete()
    return instance


class AddressMixin(models.Model):
    """
    A street address.
    """
    street = models.CharField(max_length=1024, blank=True, null=True, default=None)
    city = models.ForeignKey(
        'City', blank=True, null=True, default=None,
        related_name='%(app_label)s_%(class)s_address_city')
    state = models.ForeignKey(
        'State', blank=True, null=True, default=None,
        related_name='%(app_label)s_%(class)s_address_state')
    zip_code = models.ForeignKey(
        'ZipCode', blank=True, null=True, default=None,
        related_name='%(app_label)s_%(class)s_address_zip_code')

    class Meta:
        abstract = True

'''
class Precinct(Locality):
    """
    The smallest unit of geographic area for voters. Your precinct determines
    who and what you vote on.
    """
    number = models.CharField(
        max_length=5,
        help_text="the precinct's number e.g., 32 or 32A "
                  "(alpha characters are legal)."
    )
    zip_code = models.ForeignKey('ZipCode')


@python_2_unicode_compatible
class PSA(Locality):
    """
    """
    code = models.IntegerField()
    title = models.CharField(
        max_length=1024,
    )
    city = models.ForeignKey('City', null=True)
    county = models.ForeignKey('County', null=True)
    state = models.ForeignKey('State', null=True)
    zip_code = models.ForeignKey('ZipCode', null=True)

    def __str__(self):
        return "%d: %s" % (self.zip_code, self.city.name)
'''
