__version__ = (2, 2, '10a')

def version():
    """display version with dots"""
    return '.'.join(str(v) for v in __version__)


default_app_config = 'generator.apps.SuitConfig'
