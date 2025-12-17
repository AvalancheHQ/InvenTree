"""
Pytest configuration for InvenTree benchmarks.

This file sets up Django for benchmark tests.
"""

import os
import sys
from pathlib import Path

import django
from django.conf import settings

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent / 'src' / 'backend'
sys.path.insert(0, str(backend_dir))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InvenTree.settings')

# Setup Django
if not settings.configured:
    django.setup()
