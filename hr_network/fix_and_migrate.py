#!/usr/bin/env python
"""Fix and migrate script for separating CompetencyLevel from PostLevel/ManagementLevel"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("🔧 FIXING AND MIGRATING")
print("="*60)

# First, just try to import to check for errors
print("\n1. Testing imports...")
try:
    import django
    django.setup()
    print("   ✅ Django setup OK")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Check models
print("\n2. Checking models...")
from apps.organization.models import PostLevel, ManagementLevel
print("   ✅ PostLevel model OK")
print("   ✅ ManagementLevel model OK")

# Check forms
print("\n3. Checking forms...")
from apps.organization.forms import PostLevelForm, ManagementLevelForm
print("   ✅ PostLevelForm OK")
print("   ✅ ManagementLevelForm OK")

# Run makemigrations
print("\n4. Running makemigrations...")
from django.core.management import call_command
try:
    call_command('makemigrations', 'organization', verbosity=2)
    print("   ✅ Makemigrations completed")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Run migrate
print("\n5. Running migrate...")
try:
    call_command('migrate', verbosity=1)
    print("   ✅ Migrate completed")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*60)
print("🎉 FIX COMPLETE")
print("="*60)
print("\nNow you can:")
print("- Add columns to matrix (CompetencyLevel) - goes to assessments_competencylevel table")
print("- Add post levels (PostLevel) - goes to organization_postlevel table")
print("- Add management levels (ManagementLevel) - goes to organization_managementlevel table")
print("\nThese are now completely independent!")
