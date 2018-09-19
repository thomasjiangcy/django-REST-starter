def pytest_configure():
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.test')
    try:
        import django
        django.setup()
    except AttributeError:
        pass
