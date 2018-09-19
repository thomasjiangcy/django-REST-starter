"""
Tests to ensure Celery is setup properly.
"""

from unittest.mock import MagicMock, patch

from django.apps import apps
from django.test import TestCase

from app import taskapp
from app.taskapp.celery import CeleryConfig


class TestCeleryConfig(TestCase):

    def test_celery_config(self):
        self.assertEqual(CeleryConfig.name, 'app.taskapp')
        self.assertEqual(apps.get_app_config('taskapp').name, 'app.taskapp')

    @patch('celery.Celery.autodiscover_tasks')
    @patch('django.apps.apps.get_app_configs')
    @patch('celery.Celery.config_from_object')
    def test_celery_ready(self, config_from_object, get_app_configs, autodiscover_tasks):
        with self.settings(RAVEN_CONFIG={'dsn': 'some-dsn'}):
            patch_modules = {
                'raven': MagicMock(),
                'raven.contrib': MagicMock(),
                'raven.contrib.celery': MagicMock(),
            }
            with patch.dict('sys.modules', **patch_modules):
                config = CeleryConfig('taskapp', taskapp)
                config.ready()
                config_from_object.assert_called_with('django.conf:settings', namespace='CELERY')
                get_app_configs.assert_called()
                autodiscover_tasks.assert_called()
