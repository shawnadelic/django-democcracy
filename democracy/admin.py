from django.contrib import admin


class PollChoiceInline(admin.TabularInline):
    def __init__(self, choice_model, parent_model, admin_site, extra):
        self.model = choice_model
        self.extra = extra
        super(PollChoiceInline, self).__init__(parent_model, admin_site)


class PollBaseAdmin(admin.ModelAdmin):
    model = None
    choices_extra = 1

    def __init__(self, *args, **kwargs):
        self.model = self.poll_class
        super(PollBaseAdmin, self).__init__(*args, **kwargs)

    def get_inline_instances(self, request, obj=None):
        inline = PollChoiceInline(
            self.choice_class, self.model, self.admin_site, self.choices_extra
        )
        if request:
            if not (
                inline.has_add_permission(request) or
                inline.has_change_permission(request, obj) or
                inline.has_delete_permission(request, obj)
            ):
                inline.max_num = 0

        return [inline]
