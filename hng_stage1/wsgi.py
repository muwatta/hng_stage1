import os
import sys
from pathlib import Path

# Ensure the Django project package is importable when this file is executed
# as a Vercel Serverless Function from inside the package directory.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hng_stage1.settings')

application = get_wsgi_application()
app = application

if os.environ.get('VERCEL'):
    try:
        call_command('migrate', '--noinput')
    except Exception:
        pass
