import json
from django.conf import settings
from rest_framework.exceptions import PermissionDenied, APIException

class WorkflowConflict(APIException):
    status_code = 409
    default_detail = "Invalid workflow transition"
    default_code = "workflow_conflict"


def load_workflow_rules():
    path = settings.BASE_DIR / "apps/workflow/workflow_rules.json"
    with open(path) as f:
        return json.load(f)


def validate_workflow(entity, from_status, to_status, role, context=None):
    context = context or {}
    rules = load_workflow_rules()

    if entity not in rules:
        raise WorkflowConflict("Workflow entity not defined")

    entity_rules = rules[entity]

    if from_status not in entity_rules:
        raise WorkflowConflict("Current status not allowed")

    rule = entity_rules[from_status]

    if to_status not in rule["next"]:
        raise WorkflowConflict("Invalid status transition")

    if role.lower() != rule["role"]:
        raise PermissionDenied("Role not allowed for this transition")

    for condition in rule.get("conditions", []):
        if not context.get(condition, False):
            raise WorkflowConflict(f"Condition failed: {condition}")
