#!/usr/bin/env python
"""System health check script"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

print("="*60)
print("SYSTEM HEALTH CHECK")
print("="*60)

# 1. Check database
print("\n1. Database Check:")
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cursor.fetchall()]
print(f"   Total tables: {len(tables)}")
key_tables = [
    'assessments_competencylevel',
    'assessments_competency',
    'assessments_postcompetency',
    'interviews_interview',
    'interviews_interviewparticipant',
    'interviews_interviewevaluation',
    'organization_organizationalpost',
    'organization_person'
]
for t in key_tables:
    exists = t in tables
    print(f"   {'✓' if exists else '✗'} {t}")

# 2. Check PostCompetency columns
print("\n2. PostCompetency Columns:")
cursor.execute("PRAGMA table_info(assessments_postcompetency)")
columns = [c[1] for c in cursor.fetchall()]
for col in ['id', 'post_id', 'competency_id', 'level_id', 'is_active', 'weight', 'created_at']:
    exists = col in columns
    print(f"   {'✓' if exists else '✗'} {col}")

# 3. Check OrganizationalPost columns
print("\n3. OrganizationalPost Columns:")
cursor.execute("PRAGMA table_info(organization_organizationalpost)")
columns = [c[1] for c in cursor.fetchall()]
for col in ['id', 'title', 'department_id', 'parent_post_id', 'competency_level_id', 'description']:
    exists = col in columns
    print(f"   {'✓' if exists else '✗'} {col}")

# 4. Check migration status
print("\n4. Migration Status:")
cursor.execute("SELECT app, name FROM django_migrations ORDER BY app, name")
migrations = [f"{r[0]}.{r[1]}" for r in cursor.fetchall()]
key_migrations = [
    'assessments.0004_postcompetency',
    'assessments.0007',
    'interviews.0002',
    'organization.0008'
]
for m in key_migrations:
    applied = any(m in mig for mig in migrations)
    print(f"   {'✓' if applied else '✗'} {m}")

# 5. Check models
print("\n5. Model Check:")
from apps.assessments.models import PostCompetency, CompetencyLevel
from apps.organization.models import OrganizationalPost
from apps.interviews.models import Interview, InterviewParticipant, InterviewEvaluation

print(f"   PostCompetency fields: {list(PostCompetency._meta.get_fields())}")
print(f"   OrganizationalPost has competency_level: {hasattr(OrganizationalPost, 'competency_level')}")

print("\n" + "="*60)
print("CHECK COMPLETE")
print("="*60)
