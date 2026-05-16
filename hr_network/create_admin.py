#!/usr/bin/env python
"""Create admin user script"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create admin user if doesn't exist
email = 'admin@demo.com'
password = 'Pwd_1234'

if User.objects.filter(email=email).exists():
    print(f"⚠️  User with email {email} already exists.")
    user = User.objects.get(email=email)
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f"✅ Updated password for {email}")
else:
    user = User.objects.create_superuser(
        username='admin',
        email=email,
        password=password,
        first_name='Admin',
        last_name='User'
    )
    print(f"✅ Created superuser:")
    print(f"   Email: {email}")
    print(f"   Password: {password}")

print("\n🎉 Done! You can now login.")
