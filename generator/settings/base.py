""" #{{{ Header
Django settings for jaxid_generator project.

Creator: Benjamin Leopold (cometsong)
Created: 2015-11-19
""" #}}}

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HTML_DIR = '/var/www/html'

### Debugging {{{
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# }}}

### Allowed Hosts {{{
ALLOWED_HOSTS = [
    #'*',
    '127.0.0.1',
    'localhost',
    'mbiomecore',
    'mbiomecore.jax.org',
    # 'ctmbioc01ld',
    # 'ctmbioc01ld.jax.org',
] # }}}

### Application definition {{{
APP_NAME = 'jaxid_generator'
ROOT_URLCONF = 'generator.urls'
WSGI_APPLICATION = 'generator.wsgi.application'
import generator
APP_VERSION = generator.version()
# }}}

### Database {{{
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': { 'read_default_file': os.path.join(BASE_DIR, 'dbs', 'db.my.cnf'),
                     'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                     'charset': 'utf8mb4',
                   }
        },
    }
# }}}

### Internationalization {{{
LANGUAGE_CODE = 'en'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
# USE_TZ = True
USE_TZ = False # for functional admin_logentries app
# }}}

### Static files (CSS, JavaScript, Images) {{{
STATIC_URL = '/{}/static/'.format(APP_NAME)
STATIC_ROOT = '/var/www/html/{}/static'.format(APP_NAME)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'id_generate', 'static'),
)
# }}}


### Import Generated file path (subdir to HTML_DIR) {{{
IMPORTED_FILE_PATH = 'jaxid_generated_files'
# }}}

### Templates and Middleware {{{
MIDDLEWARE = [
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.security.SecurityMiddleware',
	]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

# }}}

### Installed Apps {{{
INSTALLED_APPS = [
    'generator',
    'id_generate',

    # 3rd party
    'django_databrowse',
    'admin_log_entries',
    'compressor',
    'django_tables2',
    'import_export',
    'django_select2',
    'django_mysql',

    # core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ]
# }}}

### App Settings {{{

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

IMPORT_EXPORT_USE_TRANSACTIONS = True

# }}}

## Secure Server {{{
SECURE_HSTS_SECONDS = ['localhost']
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
#}}}

## Site Admins {{{
ADMINS = [
    ('Benjamin', 'benjamin.leopold@jax.org'),
    ]
#}}}

# vim: set fdm=marker :#
