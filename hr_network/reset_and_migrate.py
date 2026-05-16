#!/usr/bin/env python
import os
import sys
import shutil

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Delete database
if os.path.exists('db.sqlite3'):
    os.remove('db.sqlite3')
    print("✓ Database deleted")

# Clear migration caches
for root, dirs, files in os.walk('apps'):
    if '__pycache__' in dirs:
        cache_path = os.path.join(root, '__pycache__')
        try:
            shutil.rmtree(cache_path)
        except:
            pass

print("✓ Cache cleared")

# Now run Django
import django
django.setup()

from django.core.management import call_command

print("\n🔄 Running migrations...")
try:
    call_command('migrate', verbosity=1, interactive=False)
    print("\n✅ Migrations completed successfully!")
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)

print("\n📊 Migration status:")
call_command('showmigrations', verbosity=0)
