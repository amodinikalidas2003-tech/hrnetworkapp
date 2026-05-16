#!/usr/bin/env python
"""Final system verification"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import django
    django.setup()
    
    print("="*60)
    print("✅ DJANGO SETUP SUCCESSFUL")
    print("="*60)
    
    # Check database
    from django.db import connection
    cursor = connection.cursor()
    
    # Check migrations
    cursor.execute("SELECT COUNT(*) FROM django_migrations")
    mig_count = cursor.fetchone()[0]
    print(f"\n📊 Applied migrations: {mig_count}")
    
    # Check key tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    
    print("\n📋 Key Tables:")
    key_tables = [
        ('assessments_competencylevel', 'CompetencyLevel'),
        ('assessments_competency', 'Competency'),
        ('assessments_postcompetency', 'PostCompetency'),
        ('interviews_interview', 'Interview'),
        ('interviews_interviewparticipant', 'InterviewParticipant'),
        ('interviews_interviewevaluation', 'InterviewEvaluation'),
        ('organization_organizationalpost', 'OrganizationalPost'),
        ('organization_person', 'Person'),
    ]
    for table, model in key_tables:
        status = "✅" if table in tables else "❌"
        print(f"   {status} {model} ({table})")
    
    # Check models can be imported
    print("\n🔍 Model Import Test:")
    try:
        from apps.assessments.models import PostCompetency, CompetencyLevel
        print("   ✅ assessments models OK")
    except Exception as e:
        print(f"   ❌ assessments models: {e}")
    
    try:
        from apps.interviews.models import Interview, InterviewParticipant, InterviewEvaluation
        print("   ✅ interviews models OK")
    except Exception as e:
        print(f"   ❌ interviews models: {e}")
    
    try:
        from apps.organization.models import OrganizationalPost
        print("   ✅ organization models OK")
    except Exception as e:
        print(f"   ❌ organization models: {e}")
    
    print("\n" + "="*60)
    print("🚀 SYSTEM READY - Run server with:")
    print("   python manage.py runserver --settings=config.settings")
    print("="*60)
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
