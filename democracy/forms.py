from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect

from .models import PollBase, PollChoiceBase
from .utils import get_user_hash


class PollChoiceForm(ModelForm):
    class Meta:
        model = PollChoiceBase
        exclude = ()


class PollForm(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset=None,
        label="",
    )

    def __init__(self, poll, request, *args, **kwargs):
        super(PollForm, self).__init__(*args, **kwargs)
        self.poll = PollBase.objects.get(pk=poll)
        self.user_hash = get_user_hash(request)
        kwargs = {}
        if self.poll.max_choices == 1:
            field = forms.ModelChoiceField
            widget = RadioSelect
            kwargs["empty_label"] = None
        else:
            field = forms.ModelMultipleChoiceField
            widget = CheckboxSelectMultiple
        self.fields["choices"] = field(
            queryset=self.poll.choices,
            widget=widget,
            **kwargs
        )

    def clean(self):
        cleaned_data = super(PollForm, self).clean()
        choices = cleaned_data.get("choices", None)
        poll = self.poll
        min_choices = poll.min_choices
        max_choices = poll.max_choices
        if choices:
            if isinstance(choices, PollChoiceBase):
                choices = [choices]
            num_choices = len(choices)
        else:
            raise forms.ValidationError("No choices selected")
        if min_choices and num_choices < min_choices:
            raise forms.ValidationError(
                "You selected {num_choices} item(s), which is below the min {min_choices} choice(s)."
                .format(num_choices=num_choices, min_choices=min_choices)
            )
        if num_choices > max_choices:
            raise forms.ValidationError(
                "You selected {num_choices} item(s), which is above the max {max_choices} choice(s)."
                .format(num_choices=num_choices, max_choices=max_choices)
            )
        # Check to make sure user hasn't voted within time frame
        if poll.user_hash_can_vote(self.user_hash):
            poll.add_votes(choices, self.user_hash)
            return cleaned_data
        else:
            raise forms.ValidationError(
                "You must wait at least ________ years to vote again!"
            )
