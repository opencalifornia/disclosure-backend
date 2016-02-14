import numpy as np

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
# @receiver(post_save, sender=Locality)
# @receiver(post_save, sender=City)
# @receiver(post_save, sender=County)


class DedupeQuerySet(models.QuerySet):
    def get(self, *args, **kwargs):
        dedupe_prop = self.model.dedupe_prop_name

        if np.any([key.startswith('%s__' % dedupe_prop) for key in kwargs]):
            raise NotImplementedError("%s__ attributes." % dedupe_prop)

        try:
            return super(DedupeQuerySet, self).get(*args, **kwargs)
        except ObjectDoesNotExist as odne:
            # Already did our best; stick with the exception.
            if (dedupe_prop not in kwargs or
                    np.any([key.startswith('aliases') in kwargs])):
                raise

        # Try augmented search
        prop_val = kwargs.pop(dedupe_prop)
        query = models.Q(aliases__contains=',%s,' % prop_val)
        query |= models.Q(aliases__startswith='%s,' % prop_val)
        query |= models.Q(aliases__endswith=',%s' % prop_val)
        args += (query,)
        try:
            return super(DedupeQuerySet, self).get(*args, **kwargs)
        except MultipleObjectsReturned:
            raise odne  # go with original error; clearer to users.


class DedupeAliasManager(models.Manager):
    def get_queryset(self):
        return DedupeQuerySet(self.model, using=self._db)


class DedupeMixin(models.Model):
    """
    """
    aliases = models.CharField(max_length=4096, blank=True, null=True, default=None,
                               help_text="Comma-separated list of alternate spellings")

    objects = models.Manager()
    aliased_objects = DedupeAliasManager()

    @classmethod
    def prop_is_aliased(cls, prop_val):
        if prop_val is None:
            return False
        for model in cls.objects.filter(aliases__contains=prop_val):
            if prop_val in model.aliases.split(','):
                return True
        return False

    def clean(self):
        """Make aliases unique & clean."""
        if self.aliases is not None:
            aliases_set = set([a.strip()
                               for a in self.aliases.strip().split(',')])
            aliases_cleaned = ','.join(aliases_set)
            self.aliases = aliases_cleaned or None  # convert blank to None
        return super(DedupeMixin, self).clean()

    def save(self, *args, **kwargs):
        self.clean()
        if self.prop_is_aliased(getattr(self, self.dedupe_prop_name)):
            raise Exception('No fair saving an aliased %s!' % self.dedupe_prop_name)
        super(DedupeMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


@transaction.atomic
def update_aliases(sender, instance, **kwargs):
    """Merge Dedupe models on obj1.(prop_name) in obj2.aliases"""
    if instance.aliases:
        current_aliases = []
        new_aliases = instance.aliases.split(',')

        # Resolve which models have a (prop_name) that is
        # now an alias.
        remote_models = [obj
                         for a in new_aliases
                         for obj in sender.objects.filter(
                             **{'%s__iexact' % instance.dedupe_prop_name: a})]
        if len(remote_models) == 1 and remote_models[0].aliases:
            # Remote model already has aliases, so flip things:
            # Call that the instance, and make the instance
            #   one of the remote models
            new_aliases = [getattr(instance, sender.dedupe_prop_name)]
            instance, remote_models = remote_models[0], [instance]
            current_aliases = instance.aliases.split(',')

        # Migrate any foreign keys off of aliases, then delete.
        for model in remote_models:
            for relationship in model._meta.related_objects:
                attr = relationship.name
                if hasattr(model, attr):
                    for obj in getattr(model, attr).get_queryset():
                        setattr(obj, relationship.field.name, instance)
            model.delete()  # Remove the (now obsolete) aliased model.

        # Normalize aliases
        all_aliases = current_aliases + new_aliases
        all_aliases_text = ','.join(all_aliases)
        if instance.aliases != all_aliases_text:
            instance.aliases = all_aliases_text
            instance.save()

    return instance


def dedupe(prop_name):
    def decorator(cls):
        cls.dedupe_prop_name = prop_name
        # MyClass = type(cls.__name__, (cls,), dict(prop_name=prop_name, __module__=cls.__module__))
        receiver(post_save, sender=cls)(update_aliases)
        return cls
    return decorator
