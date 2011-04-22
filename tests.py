import os
import sys
import unittest
import doctest
import django

def main():
    """
    Standalone django model test with a 'memory-only-django-installation'.
    You can play with a django model without a complete django app installation.
    http://www.djangosnippets.org/snippets/1044/
    """
    os.environ["DJANGO_SETTINGS_MODULE"] = "django.conf.global_settings"
    from django.conf import global_settings

    global_settings.INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'beproud.django.notify',
    )
    global_settings.DATABASE_ENGINE = "sqlite3"
    global_settings.DATABASE_NAME = ":memory:"
    #global_settings.ROOT_URLCONF = 'notify.tests.urls'

    global_settings.BPNOTIFY_MEDIA = {
        "news": {
            "verbose_name": "News",
            "default_types": ("new_user", "follow", "private_msg"),
            "backends": (
                "beproud.django.notify.backends.model.ModelBackend",
            ),
        },
        "private_msg": {
            "verbose_name": "Private Message",
            "default_types": ("private_msg",),
            "backends": (
                "beproud.django.notify.backends.model.ModelBackend",
                "beproud.django.notify.backends.mail.MailBackend",
            ),
        },
    }
    global_settings.BPNOTIFY_SETTINGS_STORAGE=''

    from django.test.utils import get_runner
    test_runner = get_runner(global_settings)

    if django.VERSION > (1,2):
        test_runner = test_runner()
        failures = test_runner.run_tests(['notify'])
    else:
        failures = test_runner(['notify'], verbosity=1)
    sys.exit(failures)

if __name__ == '__main__':
    main()