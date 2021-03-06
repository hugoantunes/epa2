# -*- coding: utf-8 -*-
# Django settings for SimulaPass project.

import os.path
PROJECT_ROOT = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Hugo Antunes', 'hugo.santunes@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
      'default': {
      'ENGINE': 'django.db.backends.mysql',       # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
      'NAME': 'simulapass',                       # Or path to database file if using sqlite3.
      'USER': 'root',                             # Not used with sqlite3.
      'PASSWORD': '',                         # Not used with sqlite3.
      'HOST': '127.0.0.1',                        # Set to empty string for localhost. Not used with sqlite3.
      'PORT': '3306',                             # Set to empty string for default. Not used with sqlite3.
    }
}

# DATABASES = {
#       'default': {
#       'ENGINE': 'sqlite3',       # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#       'NAME': 'simulapass',                       # Or path to database file if using sqlite3.
#       'USER': '',                             # Not used with sqlite3.
#       'PASSWORD': '',                         # Not used with sqlite3.
#       'HOST': '',                        # Set to empty string for localhost. Not used with sqlite3.
#       'PORT': '',                             # Set to empty string for default. Not used with sqlite3.
#     }
# }


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-br'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'


# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'n&1wyptqpx9o3plhwbd5wz#uw6x9nalhuo@ay6yqo@=v(!xd7@'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'SimulaPass.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
	'django.contrib.admin',
    'django_websocket', 
	
	'south',
	'passageiros',
	'transportes',
    'mundo',
    'mega_evento'

    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
TESTS_APPS = ('django_nose',)
NOSE_ARGS = ['--quiet', "-s", '--nologcapture', '--with-coverage','--cover-package=passageiros,transportes,SimulaPass']
