from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'
    verbose_name = "图片"

    def ready(self):
        import images.signals
