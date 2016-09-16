from django.db import models

from democracy.models import (
    PollChoiceModelMixin, PollModelMixin
)


class SimplePoll(PollModelMixin, models.Model):
    text = models.CharField(max_length=120)


class SimplePollChoice(PollChoiceModelMixin, models.Model):
    poll = models.ForeignKey(SimplePoll, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=120)
