"""
WSGI config for smartshop project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartshop.core.settings')

application = get_wsgi_application()
