from django.core.wsgi import get_wsgi_application
import os
import sys
from dotenv import load_dotenv

path = '/home/srcommand/SRCommand'  # '/home/<your-username>/SRCommand
if path not in sys.path:
    sys.path.insert(0, path)

load_dotenv(os.path.join(path, '.env'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'srdctwitchbot.server_settings'

# then:
application = get_wsgi_application()
