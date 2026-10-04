

def draft_report_v1(flagged_regions, metrics):
    report = []
    all_regions = []

    for transition in flagged_regions:
        for region in flagged_regions[transition]:
            if region not in all_regions:
                all_regions.append(region)

    for region in all_regions:
        periods = []
        insights = []
        implications = []

        for transition in flagged_regions:
            if region in flagged_regions[transition]:
                change = metrics[region][transition]
                periods.append(transition)
                insights.append(f"{transition}: {change:+.2f}%")

                if change > 0:
                    implications.append(
                        f"Review the underlying order records and category-level sales for {transition} to investigate the increase before deciding on operational action."
                    )
                else:
                    implications.append(
                        f"Review the underlying order records and category-level sales for {transition} to investigate the decrease before deciding on operational action."
                    )

        context = (
            f"{region} was flagged for a sales change exceeding the "
            f"8% operational alert threshold "
            f"in {', '.join(periods)}."
        )

        report.append({
            "region": region,
            "Context": context,
            "Insight": "; ".join(insights),
            "Implication": " ".join(implications)
        })

    return report
