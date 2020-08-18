from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class AppConfig(AppConfig):
    name = 'App'

    # def ready(self):
    #     autodiscover_modules('pre_executed.py')
