# Django settings

DEBUG = False
TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'America/New_York'

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'hopscotch.dram.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    
    # hopscotch apps
    'hopscotch.dram',
)