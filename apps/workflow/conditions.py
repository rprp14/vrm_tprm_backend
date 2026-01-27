def assessment_submitted(context):
    return context.get("assessment_status") == "submitted"

def same_org(context):
    return context.get("org_id") == context.get("user_org")
def has_required_evidence(context):
    return context.get("has_required_evidence", False)


def has_mandatory_answers(context):
    return context.get("has_mandatory_answers", False)


def remediation_evidence_uploaded(context):
    return context.get("evidence_uploaded", False)
