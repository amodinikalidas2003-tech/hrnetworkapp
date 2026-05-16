#!/usr/bin/env python
"""Full reset and migration script"""
import os
import sys
import shutil

# Change to project directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("STEP 1: Cleaning up...")
print("="*60)

# Delete database
if os.path.exists('db.sqlite3'):
    os.remove('db.sqlite3')
    print("✓ Database deleted")
else:
    print("- No database to delete")

# Clear all pycache
for root, dirs, files in os.walk('apps'):
    if '__pycache__' in dirs:
        try:
            shutil.rmtree(os.path.join(root, '__pycache__'))
        except:
            pass
print("✓ Cache cleared")

print("\n" + "="*60)
print("STEP 2: Setting up Django...")
print("="*60)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

print("✓ Django setup complete")

print("\n" + "="*60)
print("STEP 3: Running migrations...")
print("="*60)

from django.core.management import call_command

try:
    call_command('migrate', verbosity=1, interactive=False)
    print("\n✅ Migrations completed successfully!")
except Exception as e:
    print(f"\n❌ Migration error: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("STEP 4: Checking makemigrations...")
print("="*60)

try:
    call_command('makemigrations', '--check', verbosity=1)
    print("✅ No pending migrations to create")
except SystemExit:
    print("⚠️  Pending migrations exist (non-critical)")
except Exception as e:
    print(f"ℹ️  Makemigrations check: {e}")

print("\n" + "="*60)
print("✅ ALL DONE - System ready!")
print("="*60)
print("\nYou can now run:")
print("  python manage.py runserver --settings=config.settings")
