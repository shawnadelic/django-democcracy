from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import (
    PollBase, PollChoiceBase, PollChoiceModelMixin, PollModelMixin
)


@receiver(post_save)
def create_poll_choice(sender, instance, created, **kwargs):
    if not isinstance(instance, PollChoiceModelMixin) and created:
        pass
        # Create a poll choice


@receiver(post_delete)
def delete_poll_choice(sender, instance, **kwargs):
    if not isinstance(instance, PollChoiceModelMixin):
        return
    # Delete a poll choice


@receiver(post_save)
def create_poll(sender, instance, created, **kwargs):
    if not isinstance(instance, PollModelMixin):
        return
    if created:
        content_type = ContentType.objects.get_for_model(sender)
        PollBase.objects.create(
            content_type=content_type, object_id=instance.id
        )
        # Create a poll
    else:
        pass
        # Edit a poll, maybe sync choices?
