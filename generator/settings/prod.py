from .base import *

ALLOWED_HOSTS = [
    'mbiome_core.jax.org',
    'ctmbioc01ld.jax.org',
]

# Production SECRET_KEY
with open(os.path.join(BASE_DIR, 'secret.key')) as f:
    SECRET_KEY = f.read().strip()

SECURE_HSTS_PRELOAD = True
DEBUG = True
