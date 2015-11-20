from .base import *

# Production SECRET_KEY
with open(os.path.join(BASE_DIR, 'secret.key')) as f:
    SECRET_KEY = f.read().strip()

DEBUG = False
