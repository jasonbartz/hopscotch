import os
from mongoengine import connect

dirname = os.path.dirname

PROJECT_ROOT = os.path.abspath(os.path.join(dirname(__file__),".."))

ROOT_URLCONF = 'hopscotch.dram.urls'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
	'/Users/bartz/Code/repo/hopscotch/hopscotch/dram/templates',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'debug_toolbar.middleware.DebugToolbarMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
	'hopscotch.dram.context_processors.static',
	'django.contrib.auth.context_processors.auth',

)
DEBUG = True
INTERNAL_IPS = ('127.0.0.1',)
SECRET_KEY = 'face'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SESSION_ENGINE = 'mongoengine.django.sessions'
LOGIN_REDIRECT_URL = '/user/admin'
INSTALLED_APPS = (
	'django.contrib.sessions',
	'hopscotch.dram',
	'debug_toolbar',
)
# MongoEngne
connect('hopscotch')

AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)

CONFIG_JSON = 'config.json.local'
