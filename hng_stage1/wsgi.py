# hng_stage1/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hng_stage1.settings')

application = get_wsgi_application()