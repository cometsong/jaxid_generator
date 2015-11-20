try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

    config = {
        'description': 'The coolest jaxid_generator project!',
        'author': 'Benjamin Leopold (cometsong)',
        'url': 'URL to get it at.',
        'download_url': 'Where to download it.',
        'author_email': 'benjamin(at)cometsong(dot)net',
        'version': '0.1',
        'install_requires': ['nose'],
        'packages': ['jaxid_generator'],
        'scripts': [],
        'name': 'jaxid_generator'
    }

    setup(**config)
