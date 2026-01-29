✅ Workflow QA Checklist (Final)
🔐 Authentication & Authorization
Positive

Login with valid credentials → 200 OK

Access API with valid JWT → 200 OK

Negative

Access API without token → 401 Unauthorized

Access API with expired token → 401 Unauthorized

Vendor accessing reviewer-only API → 403 Forbidden

Reviewer accessing admin-only API → 403 Forbidden

🏢 Tenant Isolation
Negative

Vendor accesses assessment from another org → 403 Forbidden

Reviewer lists remediations from another org → 403 Forbidden

Admin (non-super) accesses cross-org data → 403 / 404

📋 Assessment Workflow
Positive

Vendor submits assessment from draft → 200 OK

Reviewer approves submitted assessment → 200 OK

Reviewer rejects submitted assessment → 200 OK

Negative

Approve assessment before submit → 409 Conflict

Vendor attempts to approve assessment → 403 Forbidden

Reviewer approves draft assessment → 409 Conflict

Approve assessment with open remediation → 409 Conflict

Repeat submit on already submitted assessment → 409 Conflict

🛠 Remediation Workflow
Positive

Reviewer creates remediation → 201 Created

Vendor starts remediation → 200 OK

Vendor submits remediation with evidence → 200 OK

Reviewer closes remediation → 200 OK

Negative

Vendor creates remediation → 403 Forbidden

Close remediation without evidence → 409 Conflict

Admin modifies remediation → 403 Forbidden

Invalid transition (open → closed) → 409 Conflict

Vendor modifies remediation from another org → 403 Forbidden

🔁 Renewal Workflow
Positive

Admin approves renewal after assessment closed → 200 OK

Admin rejects renewal → 200 OK

Negative

Trigger renewal before assessment approval → 409 Conflict

Vendor approves renewal → 403 Forbidden

Invalid renewal status jump → 409 Conflict

🌐 HTTP Method Enforcement
Negative

GET on POST-only endpoint → 405 Method Not Allowed

HEAD on workflow action endpoint → 405 Method Not Allowed

PUT on custom action endpoint → 405 Method Not Allowed

🧾 Audit Logging Verification
Positive

Successful assessment submit creates audit log

Successful remediation close creates audit log

Successful renewal approval creates audit log

Optional / Observational

Denied workflow attempt audit logging (if enabled)

📦 General API Validation
Negative

Missing required fields → 400 Bad Request

Invalid enum value for status → 400 Bad Request