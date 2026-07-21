# Sample Redacted Audit — Lead Intake and Follow-Up

> Demonstration only. Organization names, tools, volumes, and identifying details are altered. This sample shows the method and delivery standard, not a claim about a specific client result.

## Executive finding
The organization did not primarily have a lead-generation problem. It had a handoff failure: inquiries arrived through three channels, but no single record established ownership, response deadline, or closure.

## Evidence reviewed
- Shared inbox screenshots covering 14 days
- Intake spreadsheet export
- Task-board export
- Three staff interviews
- Two automation screenshots
- Ten anonymized inquiry records

## Evidence labels
- **Confirmed failure:** directly supported by records or repeated observation
- **Probable failure:** strongly supported but missing one confirming source
- **Design weakness:** structure predictably creates risk
- **Missing evidence:** cannot be determined from available material
- **Not material:** real issue with low consequence for this audit

## Current-state map

```text
Website form ─┐
Email inbox ──┼─> Staff member notices inquiry
Social DM ────┘          ↓
                  Personal follow-up method
                         ↓
            Spreadsheet OR inbox OR memory
                         ↓
              Outcome often not recorded
```

## Priority failure register

### 1. No canonical inquiry record
**Classification:** Confirmed failure  
**Evidence:** Six of ten sampled inquiries appeared in only one surface; two appeared in conflicting states across two surfaces.  
**Consequence:** The team cannot reliably distinguish new, active, waiting, closed, or lost inquiries.

### 2. Ownership is assumed rather than assigned
**Classification:** Confirmed failure  
**Evidence:** Staff described different rules for who follows up; the task board contained no assigned owner for seven sampled records.  
**Consequence:** Follow-up depends on memory and availability.

### 3. Automation creates notification but not control
**Classification:** Design weakness  
**Evidence:** The automation sends an alert but does not create a canonical record, assign responsibility, or set a response deadline.  
**Consequence:** Faster awareness does not produce reliable completion.

## Repair sequence

1. Establish one inquiry record with required source, owner, received date, next action, and state.
2. Route every intake channel into that record or a controlled manual capture queue.
3. Assign a response deadline at creation.
4. Define five lifecycle states: New, Contacting, Waiting, Qualified, Closed.
5. Add a daily exception view for unowned, overdue, and stalled inquiries.
6. Measure response and resolution before adding more automation.

## Immediate repair asset

### Minimum viable inquiry record

| Field | Required rule |
|---|---|
| Inquiry name | Plain-language identifier |
| Source | Website, email, referral, social, other |
| Owner | One accountable person |
| Received | Original timestamp |
| State | New, Contacting, Waiting, Qualified, Closed |
| Next action | One visible action |
| Response due | Time-bound deadline |
| Evidence link | Source email, form, or message |
| Closure reason | Required when closed |

### Exception view
Show any inquiry that is:
- Unassigned
- Past response deadline
- Waiting more than five business days
- Missing a next action
- Closed without a closure reason

## What not to do
- Do not add a second CRM before proving the operating rule.
- Do not automate classification based on weak or incomplete source data.
- Do not treat a notification as an assigned task.
- Do not measure only inquiry volume; measure response and closure.

## Next three actions
1. Create the canonical inquiry record and five states.
2. Import the last 30 days of open inquiries and reconcile duplicates.
3. Run the exception view daily for two weeks before expanding automation.

## Monitoring
- Median first-response time
- Percentage with assigned owner
- Percentage with next action
- Stalled inquiries older than five business days
- Qualified and closed outcomes

## Larger engagement trigger
A Repair Sprint is appropriate only when the organization approves the canonical record, assigns an owner for operating discipline, and needs help migrating channels, configuring the system, or training the team.