"""
WSGI config for jaxid_generator project.
"""
# django virtualenv variables
path_app = "/var/www/django/jaxid_generator"
app_settings = "generator.settings.dev"
path_site_packages = path_app + "/lib/python3.4/site-packages"

# semi-global wsgi script
import os
import sys
import site

# Backup sys.path
prev_sys_path = list(sys.path)
# Add virtual environment to site directories:
site.addsitedir(path_site_packages)

# settings.py sitting at /path/to/apps/my_application
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", app_settings)
os.environ["DJANGO_SETTINGS_MODULE"] = app_settings

# start the trick
sys.path.extend([
    path_app,
    path_app + '/generator/',
    path_app + '/id_generate/',
])
# Reorder syspath
new_sys_path = [p for p in sys.path if p not in prev_sys_path]
for item in new_sys_path:
    sys.path.remove(item)
# Make sure virtual env is first
sys.path[:0] = new_sys_path

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

