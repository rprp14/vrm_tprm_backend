import json
from pathlib import Path

from django.core.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied

from apps.workflow.exceptions import WorkflowForbidden, WorkflowConflict
from apps.workflow import conditions

RULES_PATH = Path(__file__).parent / "rules.json"

with open(RULES_PATH) as f:
    WORKFLOW_RULES = json.load(f)


def validate_transition(entity, action, from_status, role, context):
    """
    entity: string (assessment | remediation | renewal)
    action: string (submit | approve | close | initiate)
    from_status: current status of object
    role: request.user.role
    context: dict of condition flags
    """

    entity_rules = WORKFLOW_RULES.get(entity)
    if not entity_rules:
        raise ValidationError("Invalid workflow entity")

    rule = entity_rules.get(action)
    if not rule:
        raise ValidationError("Invalid workflow action")

    # 1️⃣ STATE VALIDATION → 409
    if from_status not in rule["from"]:
        raise WorkflowConflict(
            f"Cannot perform '{action}' when status is '{from_status}'"
        )

    # 2️⃣ ROLE VALIDATION → 403
    if role not in rule["roles"]:
        raise WorkflowForbidden(
            f"Role '{role}' not allowed to perform '{action}'"
        )

    # 3️⃣ CONDITION VALIDATION → 400
    for condition_name in rule.get("conditions", []):
        condition_func = getattr(conditions, condition_name, None)

        if not condition_func:
            raise ValidationError(f"Unknown condition: {condition_name}")

        if not condition_func(context):
            raise ValidationError(f"Condition failed: {condition_name}")

    return True
