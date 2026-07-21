# 48-Hour Verified Systems Audit — Interruption and Recovery Protocol v0.1

## Purpose
Govern interruptions, blockers, timeouts, partial delivery, and controlled recovery without concealing schedule impact or overstating completion.

## Operating states
- READY
- ACTIVE
- DEGRADED
- BLOCKED
- PAUSED
- PARTIAL DELIVERY
- RECOVERING
- RETURNED FOR EVIDENCE
- STOPPED
- CLOSED

## Pause rule
The 48-hour clock may pause only when a required client-controlled input becomes unavailable after qualification and responsible work cannot continue without it. The clock does not pause for ordinary internal inefficiency, avoidable tool confusion, poor planning, or underestimated effort.

Every pause records the start time, reason, evidence, unaffected work, blocked work, restart condition, and revised deadline method.

## Severity
### Level 1
Recoverable internally without client impact.

### Level 2
Client clarification or alternative evidence required; unaffected work continues.

### Level 3
Clock-affecting blocker; pause and notify.

### Level 4
Stop condition involving authority, safety, unsupported claims, material scope breach, or specialist work outside the engagement.

## Timeout decisions
Choose exactly one:
- NARROW
- SUBSTITUTE
- PARTIAL DELIVERY
- RESCHEDULE
- STOP

Silence is not consent. Missing evidence is not evidence of normal operation.

## Partial-delivery standard
Partial delivery is allowed only when the delivered portion is independently useful, limitations are explicit, omitted work is not represented as complete, evidence gaps remain visible, commercial implications are stated, and the client accepts the revised basis.

## Recovery sequence
CONTAIN → DIAGNOSE → DECIDE → RESTART → VERIFY → CLOSE

## Restart gate
Restart requires verified blocker disposition, tested access, reachable authority, bounded scope, revalidated evidence, acknowledged timing, and reconciliation of duplicate or stale work.

## Completion outcomes
- FULLY COMPLETED
- CONDITIONALLY COMPLETED
- PARTIALLY DELIVERED
- RESCHEDULED
- STOPPED WITHOUT COMPLETION
- CLIENT WITHDREW

## Canonical working assets
- Protocol: https://docs.google.com/document/d/1mP_6Dk5uhyRDt0upT-vcNsJtRLYYfDOeVqfyjLBhO-s/edit
- Recovery log: https://docs.google.com/spreadsheets/d/1lewQklrZ7jIDeEMtp0RlXUYeX00X3bWkj7OraWu5xzs/edit
- Intake-to-acceptance packet: https://docs.google.com/document/d/1l0aadMHiwbJYT2UHZ2C3tx_PPSM9qR2FUSwu72MxM2U/edit
- Delivery evidence log: https://docs.google.com/spreadsheets/d/10uphheyeSsYqFf_uR5qIezUL6DboP0yLsvV_LHVDfUo/edit

## Evidence boundary
This protocol is delivery infrastructure. It does not prove customer demand, completed delivery, or service effectiveness.
