import os, sys
from gevent import monkey, wsgi

monkey.patch_socket()

sys.path.insert(0, os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.handlers.wsgi import WSGIHandler

wsgi.WSGIServer(('127.0.0.1', 8077), WSGIHandler()).serve_forever()
