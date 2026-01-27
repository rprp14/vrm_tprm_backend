def log_audit_event(user, action, entity, entity_id, org_id):
    print(
        f"[AUDIT] user={user} action={action} "
        f"entity={entity} id={entity_id} org={org_id}"
    )
