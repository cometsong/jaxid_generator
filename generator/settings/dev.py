from .base import *

DEBUG = True

APP_NAME = 'jaxid_dev'
WSGI_APPLICATION = 'generator.wsgi_dev.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': { 'read_default_file': os.path.join(BASE_DIR, 'dbs', 'db.dev.my.cnf'),
                     'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                     'charset': 'utf8mb4',
                   }
        },
    'previous': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'orig.db.sqlite3'),
        }

    }

SECRET_KEY = '4$rboj1nrj84s(o79w^^5k(88@x*s03mt0*h5j=g6-j7@r^%)%'

INSTALLED_APPS[0:0] = ['debug_toolbar']
MIDDLEWARE[0:0] = ['debug_toolbar.middleware.DebugToolbarMiddleware',]
# MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware',)
INTERNAL_IPS = ['127.0.0.1',	 # localhost
                '10.6.100.151',  # plasmid
                '10.6.18.108',   # plasmid
               ]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]
# DEBUG_TOOLBAR_CONFIG = [ ]
