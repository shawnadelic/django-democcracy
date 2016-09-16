import pytest

from democracy.models import PollBase, PollChoiceBase

from .models import SimplePoll, SimplePollChoice


@pytest.mark.django_db
def test_poll_creates_base():
    # No poll bases initially
    assert not PollBase.objects.exists()

    poll = SimplePoll.objects.create(text="Best breakfast?")
    poll_base = PollBase.objects.first()

    assert poll_base
    assert poll_base.poll == poll
    assert poll.poll_base == poll_base

    # Delete the poll
    poll.delete()

    # Make sure poll base was deleted too
    assert not PollBase.objects.exists()


@pytest.mark.django_db
def test_poll_choice_creates_base():
    # No poll choice bases initially
    assert not PollChoiceBase.objects.exists()

    poll = SimplePoll.objects.create(text="Best lunch?")
    poll_base = PollBase.objects.first()
    poll_choice = SimplePollChoice.objects.create(poll=poll, text="Waffles")
    poll_choice_base = PollChoiceBase.objects.first()

    assert poll_choice_base
    assert poll_choice_base.poll_base == poll_base
    assert poll_choice.poll_choice_base == poll_choice_base

    # Delete the poll choice
    poll_choice.delete()

    # Make sure the poll choice base was deleted too
    assert not PollChoiceBase.objects.exists()
