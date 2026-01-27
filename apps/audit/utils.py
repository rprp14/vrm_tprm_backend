from .models import AuditLog

def log_event(user, action, entity, entity_id, success=True, message=""):
    AuditLog.objects.create(
        actor=user.username,
        action=action,
        entity=entity,
        entity_id=entity_id,
        org_id=user.org_id,
        success=success,
        message=message
    )
