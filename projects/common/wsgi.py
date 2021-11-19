"""
WSGI config for lala project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os
import sys
import time
import traceback
import signal

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)
sys.path.append('/home/abdel/.virtualenvs/envGterp/lib/python2.7/site-packages')
sys.path.append('/home/abdel/.virtualenvs/envGterp/planning')
sys.path.append('/home/abdel/.virtualenvs/envGterp/planning/planning')

os.environ['DJANGO_SETTINGS_MODULE'] = "planning.settings_dev"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "planning.settings_dev")

from django.core.wsgi import get_wsgi_application

try:
    application = get_wsgi_application()
    print("WSGI without exception")

except Exception:
    print("handling WSGI exceptioni !!!!")
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)
