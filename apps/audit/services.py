def log_audit_event(actor, action, entity, entity_id, org_id):
    print(f"[AUDIT] {actor} {action} {entity} {entity_id} {org_id}")
