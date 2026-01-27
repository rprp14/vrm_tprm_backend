import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import User
from apps.assessments.models import Assessment

# Create reviewer1 user
try:
    reviewer1 = User.objects.create_user(
        username='reviewer1',
        email='reviewer1@test.com',
        password='password123',
        role='reviewer',
        org_id=1
    )
    print("✓ Created reviewer1 user")
except:
    print("• reviewer1 user already exists")

# Create an assessment in draft status
try:
    assessment = Assessment.objects.create(
        name="Test Assessment",
        status="draft",
        org_id=1
    )
    print(f"✓ Created assessment with ID {assessment.id}")
except Exception as e:
    print(f"Assessment creation issue: {e}")

print("\nSetup complete!")
