

import json
from datetime import datetime

def review_gate_v1(report, decision, reviewer_note=""):
    if not isinstance(report, dict):
        raise TypeError("Report must be a dictionary")

    if decision not in ["approve", "edit", "reject"]:
        raise ValueError("Invalid decision")

    if decision == "approve":
        external_use_allowed = True
    else:
        external_use_allowed = False

    updated_report = report.copy()
    updated_report["decision"] = decision
    updated_report["reviewer_note"] = reviewer_note
    updated_report["external_use_allowed"] = external_use_allowed

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "run_id": report.get("run_id", "unknown"),
        "region": report.get("region", "unknown"),
        "decision": decision,
        "reviewer_note": reviewer_note
    }

    with open("audit_log.jsonl", "a", encoding="utf-8") as file:
        file.write(json.dumps(log_entry) + "\n")

    return updated_report
