# Workflow QA Checklist

## Positive Scenarios
- Vendor submits assessment from draft → 200 OK
- Reviewer approves submitted assessment → 200 OK
- Vendor closes remediation with required evidence → 200 OK
- Admin activates vendor → 200 OK

## Negative Scenarios
- Approve assessment before submit → 409 Conflict
- Vendor attempts to approve assessment → 403 Forbidden
- Close remediation without evidence → 409 Conflict
- Access assessment from another org → 403 Forbidden
- Trigger renewal before assessment approval → 409 Conflict
