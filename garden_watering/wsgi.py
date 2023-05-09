"""
WSGI config for garden_watering project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garden_watering.settings')
application = get_wsgi_application()


# Add the path to your Django project to the system path
sys.path.append('/home/it/garden_watering')

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'garden_watering.settings'

# Activate the virtual environment
activate_this = '/home/it/garden_watering/venv/bin/activate_this.py'
with open(activate_this) as file:
    exec(file.read(), dict(__file__=activate_this))

# Import the Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()