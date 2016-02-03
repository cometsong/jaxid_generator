""" #{{{ Header
Django settings for ctweinstock02.jax.org jaxid_generator project.

Creator: Benjamin Leopold (cometsong)
Created: 2015-11-19
""" #}}}

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

### Secret_Key {{{
SECRET_KEY = '4$rboj1nrj84s(o79w^^5k(88@x*s03mt0*h5j=g6-j7@r^%)%'
# }}}

### Debugging {{{
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# }}}

### Allowed Hosts {{{
ALLOWED_HOSTS = [
    #'*',
    '127.0.0.1',
    'localhost',
    'ctweinstock02',
] # }}}

### Application definition {{{
ROOT_URLCONF = 'generator.urls'
WSGI_APPLICATION = 'generator.wsgi.application'
# }}}

### Database {{{
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
# }}}

### Internationalization {{{
LANGUAGE_CODE = 'en'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# }}}

### Static files (CSS, JavaScript, Images) {{{
STATIC_URL = '/jaxid_generator/static/'
STATIC_ROOT = '/var/www/html/jaxid_generator/static'

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

### Templates and Middleware {{{
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    )

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
                'django.core.context_processors.request',
                ],
            },
        },
    ]

# }}}

### Installed Apps {{{
PREREQ_APPS = [
    # core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'compressor',
    'django_tables2',
    'import_export',
    ]

PROJECT_APPS = [
    'id_generate',
    ]

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS
# }}}

### App Settings {{{
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
