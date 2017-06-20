from .base import *

APP_NAME = 'jaxid_gen_dev'
WSGI_APPLICATION = 'generator.wsgi_dev.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.jaxid.devel.sqlite3'),
        },
    }

### Secret_Key {{{
SECRET_KEY = '4$rboj1nrj84s(o79w^^5k(88@x*s03mt0*h5j=g6-j7@r^%)%'
# }}}

DEBUG = True
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_ROOT = '/var/www/apps/jaxid_generator/static-dev'
# STATICFILES_DIRS = STATICFILES_DIRS + (
#     os.path.join(BASE_DIR, 'static-dev'),
# )
