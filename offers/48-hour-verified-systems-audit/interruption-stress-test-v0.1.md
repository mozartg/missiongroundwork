# 48-Hour Verified Systems Audit — Interruption Stress Test v0.1

## Purpose
Test the interruption protocol against materially different failure cases without inventing a client outcome.

## Case 1 — Access revoked after clock start
- State: BLOCKED
- Severity: LEVEL 3
- Clock: PAUSED
- Required action: preserve last known good state, record inaccessible evidence, notify client, define tested-access restart condition.
- Forbidden: continue inferring system behavior from outdated screenshots.
- Result: PASS if no unsupported conclusions are issued.

## Case 2 — Decision authority unavailable
- State: DEGRADED, then BLOCKED if the decision is required for scope or change approval.
- Severity: LEVEL 2 or LEVEL 3
- Decision: continue unaffected evidence work; pause before unauthorized change.
- Result: PASS if the operator distinguishes research from authorized implementation.

## Case 3 — Requested repair exceeds scope
- State: STOPPED for the affected work
- Severity: LEVEL 4
- Decision: narrow to an implementation-ready packet or propose a separately authorized Repair Sprint.
- Forbidden: quietly expand a fixed 48-hour audit into a broader rebuild.
- Result: PASS if no conversion is counted without client intent and a real next step.

## Case 4 — Tool failure near deadline
- State: DEGRADED
- Severity: LEVEL 1 or LEVEL 2 depending on deliverable impact
- Decision order: substitute format, preserve evidence, disclose limitation, then partial delivery only when independently useful.
- Clock rule: internal tool failure does not automatically pause the clock.
- Result: PASS if the service absorbs ordinary internal failure rather than transferring it to the client.

## Case 5 — Evidence contradicts the initial diagnosis
- State: RETURNED FOR EVIDENCE
- Decision: revise or withdraw the finding; do not protect prior analysis.
- Result: PASS if the final handoff reflects the stronger evidence.

## Case 6 — Client requests delivery despite incomplete evidence
- State: PARTIAL DELIVERY only with explicit revised basis
- Requirements: identify original promise, completed work, withheld findings, risks, continuation options, and client acceptance.
- Result: PASS if partial delivery is not called full completion.

## Overall result
The protocol resolves all six scenarios in design simulation. This is VERIFIED_ARTIFACT evidence only. It does not prove performance in a live engagement.
