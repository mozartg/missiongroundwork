# Mission GroundWork Automation Foundation

This directory is the authoritative integration layer for outreach infrastructure. It consolidates the recovered ChatGPT/Kimi package without importing its sample leads or fictional campaign data.

## Guardrails

- No paid services, metered billing, or automatic upgrades.
- No outreach is sent without an explicit `approved` status.
- No secrets are committed to GitHub.
- Google Sheets/Baserow hold operational records; GitHub holds code, schemas, workflows, and verification evidence.
- Public-source collection must respect site terms, robots rules, rate limits, privacy, and applicable anti-spam law.

## Start the stack

```bash
cd automation
cp .env.example .env
# Replace required values in .env
docker compose config
docker compose up -d n8n baserow
```

Optional profiles:

```bash
docker compose --profile extended up -d
docker compose --profile ai-local up -d
docker compose --profile email up -d
```

## Expected local endpoints

| Service | URL | Profile |
|---|---|---|
| n8n | http://localhost:5678 | core |
| Baserow | http://localhost:8000 | core |
| Activepieces | http://localhost:8081 | extended |
| NocoDB | http://localhost:8082 | extended |
| Flowise | http://localhost:3002 | ai-local |
| Ollama | http://localhost:11434 | ai-local |
| Plunk | http://localhost:3003 | email |

## Workflow order

1. `workflow_1_import_validate.json`
2. `workflow_2_generate_drafts.json`
3. `workflow_3_approved_to_gmail_draft.json`
4. `workflow_4_send_command.json`
5. `workflow_5_followup_check.json`
6. `workflow_6_reply_unsubscribe.json`
7. `workflow_7_daily_summary.json`

The seven workflow files remain a tracked implementation task until they are imported, credentialed, tested with synthetic records, and exported back into this directory.

## Acceptance tests

1. `docker compose config` succeeds.
2. Core containers start and remain healthy.
3. A synthetic lead imports into the data layer.
4. A draft is generated but not sent.
5. Approval creates a Gmail draft first.
6. Sending requires a separate explicit command.
7. Unsubscribe/suppression prevents future sends.
8. A daily summary reports totals and failures without exposing secrets.

## Current integration boundary

Normal ChatGPT integrations can maintain GitHub, Google Drive/Sheets, Gmail drafts, Calendar, and project-management records. They cannot start Docker containers on the user's Windows machine or authorize OAuth credentials without the user completing the provider authorization screen. Those desktop/credential steps must be recorded as verified blockers rather than claimed complete.
