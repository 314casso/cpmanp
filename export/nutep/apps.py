from django.apps import AppConfig


class NutepConfig(AppConfig):
    name = "nutep"

    def ready(self):
        from nutep.signals import connect_signals
        connect_signals()
