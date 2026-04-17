# hng_stage1/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hng_stage1.settings')

# Run migrations on cold start
from django.core.management import call_command
call_command('migrate', '--no-input')

application = get_wsgi_application()