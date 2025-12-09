"""
ASGI config for smartshop project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartshop.core.settings')

application = get_asgi_application()
