"""
Workflow exceptions module.
"""
from rest_framework.exceptions import APIException


class WorkflowConflict(APIException):
    status_code = 409
    default_detail = "Invalid workflow transition"
    default_code = "workflow_conflict"


class WorkflowForbidden(APIException):
    status_code = 403
    default_detail = "Role not allowed for this workflow action"
    default_code = "workflow_forbidden"


class WorkflowForbidden(Exception):
    """Exception raised when a workflow action is forbidden."""
    pass


class WorkflowConflict(Exception):
    """Exception raised when a workflow action conflicts with the current state."""
    pass
