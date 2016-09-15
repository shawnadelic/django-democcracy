from django.db import models

from democracy.models import (
    PollBase, PollChoiceBase, PollChoiceModelMixin,
    PollModelMixin, Vote
)

class SimplePoll(PollModelMixin, models.Model):
    text = models.CharField(max_length=120)
