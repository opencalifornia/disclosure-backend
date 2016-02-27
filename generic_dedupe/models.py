from django.contrib.admin.models import LogEntry
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class DedupeManager(models.Manager):
    """Hide corrected models."""
    def get_queryset(self):
        return super(DedupeManager, self).get_queryset().filter(true_model_id=None)


class DedupeMixin(models.Model):
    """
    Adds the 'true_model_id' integer field, and swaps out managers.
    """
    objects = models.Manager()
    filtered_objects = DedupeManager()
    true_model_id = models.IntegerField(default=None, blank=True, null=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class DedupeLogEntry(LogEntry):
    """
    Log for deduped items.

    This is both for keeping records of what happens, as well as
    allowing us to undo deduping.
    """
    class_name = models.CharField(max_length=1024)
    prop_name = models.CharField(max_length=1024)
    true_model_id = models.IntegerField()
    old_true_model_id = models.IntegerField(default=None, blank=True, null=True)

    def save(self, *args, **kwargs):
        """Add a default meaningful change_message."""
        if not self.change_message:
            self.change_message = "Changed %s.%s for %s from %d to %d" % (
                self.class_name, self.prop_name, self.object_repr,
                self.old_true_model_id, self.true_model_id)
        super(DedupeLogEntry, self).save(*args, **kwargs)

    def __str__(self):
        return self.change_message

    class Meta:
        app_label = 'generic_dedupe'
