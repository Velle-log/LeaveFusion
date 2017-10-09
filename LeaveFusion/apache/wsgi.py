"""
WSGI config for LeaveFusion project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os, sys

apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)
sys.path.append(project)


proxyDict = {
              "http"  : '172.27.16.250:3128',
              "https" : '172.27.16.250:3128',
              "ftp"   : '172.27.16.250:3128'
            }

os.environ["http_proxy"] = proxyDict['http']
os.environ["https_proxy"] = proxyDict['https']
os.environ["ftp_proxy"] = proxyDict['ftp']

import logging
logging.basicConfig(stream=sys.stderr)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LeaveFusion.settings")

application = get_wsgi_application()
