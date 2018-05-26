# pylint: disable=unused-wildcard-import, wildcard-import
""" Local development """

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0qsd*-ysb@43fqy10*#&86c0iqko7s6=(3wo9dhh8p8jt_h2m0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

# STATIC_ROOT = BASE_DIR.ancestor(2).child('static')
STATIC_ROOT = '/home/netsamir/webapps/rammotors/static'

STATICFILES_DIRS = [
    BASE_DIR.child('static'),
]
