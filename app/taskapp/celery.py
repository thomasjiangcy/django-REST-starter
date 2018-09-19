"""
Celery configuration
"""

import os

from django.apps import AppConfig, apps
from django.conf import settings

from celery import Celery

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')  # pragma: no cover


app = Celery('app')


class CeleryConfig(AppConfig):
    """
    Celery configuration
    """
    name = 'app.taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        app.config_from_object('django.conf:settings', namespace='CELERY')
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)
        app.autodiscover_tasks(lambda: installed_apps, related_name='periodic_tasks', force=True)
        if hasattr(settings, 'RAVEN_CONFIG'):
            from raven import Client as RavenClient
            from raven.contrib.celery import register_signal as raven_register_signal
            from raven.contrib.celery import register_logger_signal as raven_register_logger_signal
            raven_client = RavenClient(dsn=settings.RAVEN_CONFIG['dsn'])
            raven_register_logger_signal(raven_client)
            raven_register_signal(raven_client)
