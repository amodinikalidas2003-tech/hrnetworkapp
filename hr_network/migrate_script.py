import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.core.management import call_command

print("Running migrations...")
try:
    call_command('migrate', verbosity=2)
    print("Migrations completed successfully!")
except Exception as e:
    print(f"Error during migrations: {e}")

print("\nChecking for pending makemigrations...")
try:
    call_command('makemigrations', '--check', verbosity=2)
    print("No pending migrations to create.")
except Exception as e:
    print(f"Pending migrations exist or error: {e}")
