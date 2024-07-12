# conftest.py

import pytest
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'El_Curador.settings'
django.setup()

pytestmark = pytest.mark.django_db
