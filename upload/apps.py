from django.apps import AppConfig


class UploadConfig(AppConfig):
    name = 'upload'
    def ready(self):
      from .ap_scheduler import start
      start()
