
import json
from pathlib import Path

from draft_report import draft_report_v1
from review_gate import review_gate_v1

def run_report_review():
    with open("state.json", "r", encoding="utf-8") as file:
        state = json.load(file)

    flagged_regions = {
        "Apr->May": state["april_to_may_flags"],
        "May->Jun": state["may_to_june_flags"]
    }

    metrics = {}

    for region in state["april_to_may_changes"]:
        metrics[region] = {
            "Apr->May": state["april_to_may_changes"][region],
            "May->Jun": state["may_to_june_changes"][region]
        }

    report = draft_report_v1(flagged_regions, metrics)

    print("GENERATED DRAFT REPORT")
    print("=" * 60)

    for item in report:
        print(item)
        print("-" * 60)

    print("\nHUMAN REVIEW TEST")
    print("=" * 60)

    if not report:
        print("No flagged regions to review.")
        return

    test_report = report[0].copy()
    test_report["run_id"] = "report_review_test"

    for decision in ["approve", "edit", "reject"]:
        print("\nDecision:", decision)
        print("Before review:")
        print(test_report)

        result = review_gate_v1(
            test_report,
            decision,
            reviewer_note="Test harness validation"
        )

        print("After review:")
        print(result)
        print("-" * 60)

if __name__ == "__main__":
    run_report_review()
