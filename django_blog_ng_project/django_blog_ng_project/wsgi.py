"""
WSGI config for django_blog_ng_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_blog_ng_project.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
