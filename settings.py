import os

SITE_ID            = 1
SECRET_KEY         = 'hot1!ntbc$on@ypotwo5r#e9=^)jqbmc$5s-ud8$!wk^l@p&y3'

DEBUG              = True
TEMPLATE_DEBUG     = DEBUG

ADMINS = (
	('Elena Kantemirova', 'elena.kantemirova@gmail.com'),
	('Gvidon Malyarov'  , 'nenegoro@gmail.com'),
)

MANAGERS           = ADMINS

DATABASE_ENGINE    = 'mysql'
DATABASE_NAME      = 'byhands'
DATABASE_USER      = 'root'
DATABASE_PASSWORD  = '123097'
DATABASE_HOST      = 'localhost'
DATABASE_PORT      = ''

USE_I18N           = False
TIME_ZONE          = 'Europe/Moscow'
LANGUAGE_CODE      = 'ru-ru'

PROJECT_ROOT       = '/home/nide/code/byhands'
MEDIA_ROOT         = PROJECT_ROOT+'/media/'
UPLOAD_ROOT        = PROJECT_ROOT+'/media/upload/'
MEDIA_URL          = 'http://media.byhands:8081'

ADMIN_MEDIA_PREFIX = '/admin/media/'

ROOT_URLCONF       = 'byhands.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.auth',
	'django.core.context_processors.request',
	
	'byhands.context_processors.media_url',
	'byhands.context_processors.cart',
)

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source',
	'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
    os.path.join(PROJECT_ROOT, 'apps/candy/templates'),
    os.path.join(PROJECT_ROOT, 'apps/contactus/templates'),
)

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	
	'byhands.apps.contactus',
	'byhands.apps.candy',
	'byhands.apps.candy.models',
	'byhands.apps.site',
)

