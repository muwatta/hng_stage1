import os
import sys
from pathlib import Path

# Ensure the project root is on the import path when Vercel executes this file.
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hng_stage1.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
app = application
