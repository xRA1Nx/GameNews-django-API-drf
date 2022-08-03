from django.apps import AppConfig


class GamenewsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gamenews_app'

    def ready(self):
        from . import signals

