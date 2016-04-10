from django.apps import AppConfig


class DemocracyAppConfig(AppConfig):
    name = 'democracy'
    verbose_name = "Democracy"

    def ready(self):
        import democracy.signals  # noqa
