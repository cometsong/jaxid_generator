from .base import *

DEBUG = True

APP_NAME = 'jaxid_dev'
WSGI_APPLICATION = 'generator.wsgi_dev.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.jaxid.devel.sqlite3'),
        },
    }

SECRET_KEY = '4$rboj1nrj84s(o79w^^5k(88@x*s03mt0*h5j=g6-j7@r^%)%'

