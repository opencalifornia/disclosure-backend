from django.contrib.auth.models import User
from django.contrib.admin.models import ADDITION
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver


def model_and_supers(model):
    """Return an iterator containing the model and it's superclass versions."""
    if model is None:
        return
    yield model
    for cls in model._meta.get_parent_list():
        yield cls.objects.get(id=model.id)


def get_related_queryset(model, relationship):
    """Drills into relationship to pull out related models."""
    if relationship.one_to_one:
        return []

    attr = relationship.get_accessor_name()
    attr_val = getattr(model, attr, None)
    queryset = attr_val.get_queryset() if attr_val else []
    return queryset


@transaction.atomic
def revert_dedupe(sender, instance, **kwargs):
    """
    Pre-save: if true_model was previously set, revert all foregn
    keys to point back to the actual model.
    """
    # Get the model as it was before save.
    try:
        old_model = sender.objects.get(id=instance.id)
    except sender.DoesNotExist:
        return
    else:
        if old_model.true_model_id is None:
            return

    true_model = sender.objects.get(id=old_model.true_model_id)

    # Loop through foreign key relationships.
    for tm in model_and_supers(true_model):
        for relationship in tm._meta.related_objects:
            for obj in get_related_queryset(tm, relationship):
                # Make sure there's a log entry setting the
                # true_model_id to true_model on this object.
                #
                # Otherwise, this is just an actual direct entry
                #   for the true model.
                from .models import DedupeLogEntry
                log_entries = DedupeLogEntry.objects.filter(
                    object_id=obj.pk,
                    old_true_model_id=instance.id, true_model_id=tm.id,
                    class_name=obj.__class__.__name__,
                    prop_name=relationship.field.name)
                if log_entries.count() == 0:
                    # print("No matching log entry for %s" % obj)
                    continue
                else:
                    # print("Need to revert for %s" % obj)
                    log_entries.delete()

                # Reset the attribute to the original value--this model instance.
                setattr(obj, relationship.field.name, instance)
                obj.save()

    return instance


@transaction.atomic
def apply_dedupe(sender, instance, **kwargs):
    """Post-save: set up any new."""
    if instance.true_model_id is not None:
        true_model = sender.objects.get(id=instance.true_model_id)
        for inst, tm in zip(model_and_supers(instance), model_and_supers(true_model)):
            # Migrate any foreign keys from the instance to the true_model
            for relationship in inst._meta.related_objects:
                for obj in get_related_queryset(inst, relationship):
                    # Add a log entry, for an auto-created user.
                    user, _ = User.objects.get_or_create(username='DedupeUser')
                    from .models import DedupeLogEntry
                    log_entry = DedupeLogEntry(
                        object_id=obj.pk, object_repr=str(obj), action_flag=ADDITION,
                        content_type_id=ContentType.objects.get_for_model(obj).pk,
                        user_id=user.id,
                        true_model_id=tm.id,
                        old_true_model_id=getattr(obj, relationship.field.name).id,
                        class_name=obj.__class__.__name__,
                        prop_name=relationship.field.name)
                    log_entry.save()

                    # Set the actual data; must be done after log as the logging
                    # assumes this value is the old value.
                    setattr(obj, relationship.field.name, tm)
                    obj.save()

    return instance


def add_dedupe_signals(cls):
    """Class decorator to add signals needed to dedupe."""
    receiver(pre_save, sender=cls)(revert_dedupe)
    receiver(post_save, sender=cls)(apply_dedupe)
    receiver(pre_delete, sender=cls)(revert_dedupe)
    return cls
