""" #{{{ Header
Django settings for ctweinstock02.jax.org jaxid_generator project.

Creator: Benjamin Leopold (cometsong)
Created: 2015-11-19
""" #}}}

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

### Debugging {{{
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# }}}

### Allowed Hosts {{{
ALLOWED_HOSTS = [
    #'*',
    '127.0.0.1',
    'localhost',
    'mbiome_core',
    'mbiome_core.jax.org',
    'ctmbioc01ld.jax.org',
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
                ],
            },
        },
    ]

# }}}

### Installed Apps {{{
ADMIN_APPS = [
    # 'jet',
    'suit',
    'django.contrib.admin',
    ]
PREREQ_APPS = [
    # core
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

INSTALLED_APPS = ADMIN_APPS + PREREQ_APPS + PROJECT_APPS
# }}}

### App Settings {{{
IMPORT_EXPORT_USE_TRANSACTIONS = True

# Django Suit configuration example
SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'Mbiome Core JAXid Generator Admin',
    'HEADER_DATE_FORMAT': 'l, d-M-o',
    'HEADER_TIME_FORMAT': 'H:i e',

    # forms
    'SHOW_REQUIRED_ASTERISK': True,  # Default True
    'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
    # 'SEARCH_URL': '/admin/auth/user/',
    # 'MENU_ICONS': {
    #    'sites': 'icon-leaf',
    #    'auth': 'icon-lock',
    # },
    # 'MENU_OPEN_FIRST_CHILD': True, # Default True
    # 'MENU_EXCLUDE': ('auth.group',),
    # 'MENU': (
    #     'sites',
    #     {'app': 'auth', 'icon':'icon-lock', 'models': ('user', 'group')},
    #     {'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
    #     {'label': 'Support', 'icon':'icon-question-sign', 'url': '/support/'},
    # ),

    # misc
    # 'LIST_PER_PAGE': 15
}

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
