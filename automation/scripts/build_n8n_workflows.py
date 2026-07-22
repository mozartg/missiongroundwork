#!/usr/bin/env python3
"""Build seven importable, credential-free n8n workflow skeletons.

The generated workflows enforce state transitions before any external connector
node is added. Gmail, Sheets, Baserow, and model credentials are intentionally
not embedded in source control.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "n8n" / "workflows.bundle.json"
OUT = ROOT / "n8n" / "workflows"


def webhook_node(name: str, path: str, x: int = 260) -> dict[str, Any]:
    return {
        "parameters": {"httpMethod": "POST", "path": path, "responseMode": "responseNode", "options": {}},
        "id": f"webhook-{path}",
        "name": name,
        "type": "n8n-nodes-base.webhook",
        "typeVersion": 2,
        "position": [x, 300],
    }


def code_node(name: str, code: str, x: int = 520) -> dict[str, Any]:
    return {
        "parameters": {"jsCode": code},
        "id": name.lower().replace(" ", "-"),
        "name": name,
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [x, 300],
    }


def respond_node(x: int = 780) -> dict[str, Any]:
    return {
        "parameters": {"respondWith": "json", "responseBody": "={{ $json }}", "options": {}},
        "id": "respond-json",
        "name": "Respond JSON",
        "type": "n8n-nodes-base.respondToWebhook",
        "typeVersion": 1.4,
        "position": [x, 300],
    }


def schedule_node(name: str, hour: int) -> dict[str, Any]:
    return {
        "parameters": {"rule": {"interval": [{"field": "hours", "hoursInterval": 24, "triggerAtHour": hour}]}},
        "id": name.lower().replace(" ", "-"),
        "name": name,
        "type": "n8n-nodes-base.scheduleTrigger",
        "typeVersion": 1.2,
        "position": [260, 300],
    }


def build(item: dict[str, Any]) -> dict[str, Any]:
    name = item["name"]
    if "path" in item:
        start = webhook_node(item["nodes"][0], item["path"])
        code = code_node(
            item["nodes"][1],
            """const input = $json.body ?? $json;
const now = new Date().toISOString();
const email = String(input.email ?? '').trim().toLowerCase();
const status = String(input.status ?? '').trim();
const suppressed = Boolean(input.suppressed || input.unsubscribe);
const errors = [];
if (input.workflow === 'import' || $workflow.name.startsWith('01')) {
  for (const key of ['first_name','organization','email']) if (!String(input[key] ?? '').trim()) errors.push(`missing:${key}`);
  if (email && !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) errors.push('invalid:email');
}
if ($workflow.name.startsWith('03') && status !== 'approved') errors.push('status_must_be_approved');
if ($workflow.name.startsWith('04') && status !== 'send_requested') errors.push('status_must_be_send_requested');
if ($workflow.name.startsWith('04') && !input.gmail_draft_id) errors.push('gmail_draft_id_required');
if (suppressed) errors.push('suppressed');
return [{json:{ok:errors.length===0, errors, received_at:now, record:{...input,email}}}];""",
        )
        nodes = [start, code, respond_node()]
        connections = {
            start["name"]: {"main": [[{"node": code["name"], "type": "main", "index": 0}]]},
            code["name"]: {"main": [[{"node": "Respond JSON", "type": "main", "index": 0}]]},
        }
    else:
        hour = 13 if name.startswith("05") else 1 if name.startswith("06") else 21
        start = schedule_node(item["nodes"][0], hour)
        code = code_node(
            item["nodes"][1],
            """return [{json:{ok:true, dry_run:true, workflow:$workflow.name, checked_at:new Date().toISOString(), note:'Attach authenticated data-source nodes after local import and credential authorization.'}}];""",
        )
        nodes = [start, code]
        connections = {start["name"]: {"main": [[{"node": code["name"], "type": "main", "index": 0}]]}}
    return {
        "name": name,
        "nodes": nodes,
        "connections": connections,
        "pinData": {},
        "settings": {"executionOrder": "v1", "saveManualExecutions": True},
        "active": False,
        "meta": {"templateCredsSetupCompleted": False, "purpose": item["purpose"], "guardrails": item["guardrails"]},
        "tags": [{"name": "mission-groundwork"}, {"name": "approval-gated"}],
        "versionId": "00000000-0000-4000-8000-000000000000",
    }


def main() -> None:
    bundle = json.loads(BUNDLE.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    for item in bundle["workflows"]:
        target = OUT / item["file"]
        target.write_text(json.dumps(build(item), indent=2) + "\n", encoding="utf-8")
        print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()
