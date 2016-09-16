from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.views.generic.base import View
from ipware.ip import get_ip, get_real_ip

from rest_framework.exceptions import APIException
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import PollForm
from .models import PollBase, PollChoiceBase
from .utils import get_user_hash


def get_user_ip(request):
    return get_real_ip(request) or get_ip(request)


class VoteResultsAPIView(APIView):
    renderer_classes = (JSONRenderer,)

    def get(self, request, votable_class, object_id, format=None):
        VotableClass = votable_class
        poll_choice_object = PollChoiceBase.objects.get(
            object_id=object_id,
            content_type=ContentType.objects.get_for_model(VotableClass)
        )
        upvotes = poll_choice_object.votes.count()
        content = {"user_ip": get_user_ip(request), "object_id": object_id, "count": upvotes}
        return Response(content)

    def post(self, request, votable_class, object_id, format=None):
        try:
            pass
            # vote_type = getattr(VoteType, vote_type_name.upper())
        except:
            raise APIException("Missing or incorrect vote type")

        # content = {"user_ip": get_user_ip(request), "vote_type": vote_type.value, "object_id": object_id}
        content = {"status": "success"}
        return Response(content)


class PollVoteView(View):
    def get(self, request, *args, **kwargs):
        poll_id = kwargs.get("poll_id")
        user_hash = get_user_hash(request)
        poll = PollBase.objects.get(pk=poll_id)
        if poll.user_hash_can_vote(user_hash):
            context = {"form": PollForm(poll_id, request)}
        else:
            context = {"results": poll.get_results(user_hash)}
        return render(request, "democracy/poll.html", context)

    def post(self, request, *args, **kwargs):
        poll_id = kwargs.get("poll_id")
        form = PollForm(poll_id, request, request.POST)
        if form.is_valid():
            messages.success(request, "Your vote was successfully received!")
        else:
            messages.error(request, "Unfortunately, there were some errors!")
        return render(request, "democracy/poll.html", {"form": form})
