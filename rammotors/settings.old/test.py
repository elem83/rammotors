# pylint: disable=unused-wildcard-import, wildcard-import

""" Allow quicker test with the :memory: settings """

from .local import *

DATABASES = {
    'default':{
        'ENGINE': "django.db.backends.sqlite3",
        'NAME': ':memory:',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
