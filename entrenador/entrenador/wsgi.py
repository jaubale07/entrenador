"""
WSGI config for entrenador project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import sys
#Wrong!
#sys.path.append("/home/user/mysite/mysite")

#Correct
#sys.path.append("/home/user/mysite")
sys.path.append("/var/www/html/entrenador")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "entrenador.settings")
application = get_wsgi_application()