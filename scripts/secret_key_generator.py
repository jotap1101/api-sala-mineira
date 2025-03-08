"""
This script generates a new secret key for the Django project.
"""

from django.core.management.utils import get_random_secret_key

print(get_random_secret_key())