from django.apps import AppConfig


class OperationsConfig(AppConfig):
    name = 'operations'
    verbose_name = "操作"

    def ready(self):
        import operations.signals
