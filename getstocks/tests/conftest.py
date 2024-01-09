# getstocks/tests/conftest.py

import os
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "getstocks.settings")
settings.configure()

import django
django.setup()

