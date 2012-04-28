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

DEBUG = True

SECRET_KEY = 'face'


# MongoEngne
connect('hopscotch')

AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)