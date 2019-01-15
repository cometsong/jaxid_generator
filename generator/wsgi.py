"""
WSGI config for jaxid_generator project.
"""
# django virtualenv variables
path_app = "/var/www/apps/jaxid_generator"
path_lib = path_app + "/lib/python3.6/site-packages"
app_settings = "generator.settings.prod"

# semi-global wsgi script
import os
import sys
import site

# settings.py sitting at /path/to/apps/my_application
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", app_settings)
os.environ["DJANGO_SETTINGS_MODULE"] = app_settings

# Make sure virtual env is first
new_sys_path = [
    path_app,
    path_app + '/generator/',
    path_app + '/id_generate/',
    path_lib,
]
new_sys_path.extend(sys.path)
# remove dupe items from list:
sys.path = list(dict.fromkeys(new_sys_path))
site.addsitedir(path_lib)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
