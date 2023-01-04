from django.apps import AppConfig
class WebConfig(AppConfig):
    name = 'web'
    def ready(self):
      from .ap_scheduler import start
      start()
