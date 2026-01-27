import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import User
from apps.assessments.models import Assessment
from rest_framework.test import APIClient

# Get or create reviewer1 user
reviewer1, created = User.objects.get_or_create(
    username='reviewer1',
    defaults={
        'email': 'reviewer1@test.com',
        'role': 'reviewer',
        'org_id': 1
    }
)
if created:
    reviewer1.set_password('password123')
    reviewer1.save()
    print("✓ Created reviewer1 user")
else:
    print("✓ Using existing reviewer1 user")

# Get or create an assessment in draft status
assessment, created = Assessment.objects.get_or_create(
    name="Test Assessment",
    defaults={
        'status': 'draft',
        'org_id': 1
    }
)
if created:
    print(f"✓ Created assessment ID {assessment.id} with status: {assessment.status}")
else:
    print(f"✓ Using existing assessment ID {assessment.id} with status: {assessment.status}")

# Test the API
client = APIClient()
client.force_authenticate(user=reviewer1)

print(f"\n🧪 Test 1: Approve before submit")
print(f"   - Assessment ID: {assessment.id}")
print(f"   - Assessment Status: {assessment.status}")
print(f"   - Logged in as: {reviewer1.username} (role: {reviewer1.role})")
print(f"   - Sending: POST /api/assessments/{assessment.id}/approve/")

response = client.post(f'/api/assessments/{assessment.id}/approve/')

print(f"\n📊 Response:")
print(f"   - Status Code: {response.status_code}")
print(f"   - Response Data: {json.dumps(response.data, indent=2)}")

if response.status_code == 409:
    print(f"\n✅ TEST PASSED: Got expected 409 Conflict!")
else:
    print(f"\n❌ TEST FAILED: Expected 409, got {response.status_code}")
