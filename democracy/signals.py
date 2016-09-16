from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (PollBase, PollChoiceBase, PollChoiceModelMixin,
                     PollModelMixin)


@receiver(post_save)
def create_poll_choice(sender, instance, created, **kwargs):
    if not isinstance(instance, PollChoiceModelMixin) and created:
        return
    if created:
        choice_content_type = ContentType.objects.get_for_model(sender)
        PollChoiceBase.objects.create(
            poll_base=instance.poll.poll_base,
            content_type=choice_content_type, object_id=instance.id
        )


@receiver(post_save)
def create_poll(sender, instance, created, **kwargs):
    if not isinstance(instance, PollModelMixin):
        return
    if created:
        poll_content_type = ContentType.objects.get_for_model(sender)
        PollBase.objects.create(
            content_type=poll_content_type, object_id=instance.id
        )
    else:
        pass
        # Edit a poll, maybe sync choices?
