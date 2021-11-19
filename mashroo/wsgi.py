"""
WSGI config for mashroo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""
import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = "mashroo.settings"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mashroo.settings')

from django.core.wsgi import get_wsgi_application

try:
    application = get_wsgi_application()

except Exception:
    print("Abdel handling WSGI exceptioni !!!!")
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)

