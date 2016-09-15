import pytest

from democracy.models import (
    PollBase, PollChoiceBase, PollChoiceModelMixin,
    PollModelMixin, Vote
)

from .models import SimplePoll

@pytest.mark.django_db
def test_poll_creates_base():
    # No poll bases initially
    assert not PollBase.objects.exists()

    poll = SimplePoll.objects.create(text="Blah blah")
    poll_base = PollBase.objects.first()

    assert poll_base.content_object == poll
    assert poll.poll_base_object.first() == poll_base
    #import pdb; pdb.set_trace()

    #poll.delete()
    #print(SimplePoll.objects.all())
    #print(PollBase.objects.all())
    #assert not PollBase.objects.exists()
