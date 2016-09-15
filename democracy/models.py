import datetime

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.transaction import atomic
from django.utils import timezone


class PollBase(models.Model):
    max_choices = models.IntegerField(default=1)
    min_choices = models.IntegerField(blank=True, null=True)
    revote_limit = models.DurationField(blank=True, default=datetime.timedelta(days=1))

    # Content type relation for models inheriting from PollModelMixin
    content_object = GenericForeignKey("content_type", "object_id")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    def __str__(self):
        return str("Poll {number}: {content_object}".format(number=self.pk, content_object=self.content_object))

    # Should be user_can_vote, and user_hash should be configurable
    def user_hash_can_vote(self, user_hash):
        # Maybe check banned user hashes?
        # last_vote = Vote.objects.order_by("-created_on").filter(user_hash=user_hash).first()
        revote_time = timezone.now() - self.revote_limit
        return not Vote.objects.order_by("-created_on").filter(user_hash=user_hash, created_on__gt=revote_time).exists()

    def add_vote(self, choice, user_hash):
        Vote.objects.create(poll=self, choice=choice, user_hash=user_hash)

    @atomic
    def add_votes(self, choices, user_hash):
        for choice in choices:
            self.add_vote(choice, user_hash)

    def get_results(self, user_hash):
        return [(choice.content_object, choice.get_vote_count(user_hash)) for choice in self.choices.all()]


class PollChoiceBase(models.Model):
    poll = models.ForeignKey("PollBase", on_delete=models.CASCADE, related_name="choices")

    # Content type relation for models inheriting from PollChoiceModelMixin
    content_object = GenericForeignKey("content_type", "object_id")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    def __str__(self):
        return "PollChoice {number}: {object}".format(number=self.pk, object=str(self.content_object))

    def get_vote_count(self, user_hash):
        return self.votes.count()


class Vote(models.Model):
    poll = models.ForeignKey(PollBase, on_delete=models.CASCADE, related_name="votes")
    choice = models.ForeignKey(PollChoiceBase, on_delete=models.CASCADE, related_name="votes")
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    user_hash = models.CharField(max_length=255)

    def __str__(self):
        return str(self.pk)


class PollChoiceModelMixin(models.Model):

    class Meta:
        abstract = True

class PollModelMixin(models.Model):
    poll_base_object = GenericRelation(
        PollBase,
        related_name="poll_object"
    )

    class Meta:
        abstract = True
