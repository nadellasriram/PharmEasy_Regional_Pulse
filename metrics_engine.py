
import json


def compute_percentage_change_v1(current, previous):
    if previous == 0:
        return 0

    return ((current - previous) / previous) * 100


def flag_significant_regions_v1(changes, threshold=8):
    flagged_regions = []

    for region, change in changes.items():
        if abs(change) > threshold:
            flagged_regions.append(region)

    return flagged_regions


def save_state_v1(state, path="state.json"):
    with open(path, "w") as file:
        json.dump(state, file, indent=4)


def load_previous_state_v1(path="state.json"):
    try:
        with open(path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
