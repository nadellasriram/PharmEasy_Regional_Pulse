
"""
generate_dataset.py -- PharmEasy Regional Pulse capstone dataset builder.
Deterministic (fixed seed = 2026): every student who runs this file unmodified
gets byte-identical pharmeasy_orders_raw.csv and regions_master.csv.
"""
import random
import csv
from collections import defaultdict

rng = random.Random(2026)

REGIONS_ACTIVE = [
    "Hyderabad", "Warangal", "Vijayawada", "Visakhapatnam",
    "Guntur", "Nellore", "Tirupati", "Karimnagar", "Bengaluru",
]
REGION_ZERO_ORDERS = "Kurnool"
REGIONS_MASTER = REGIONS_ACTIVE + [REGION_ZERO_ORDERS]
STATE_OF = {
    "Hyderabad": "Telangana", "Warangal": "Telangana", "Karimnagar": "Telangana",
    "Vijayawada": "Andhra Pradesh", "Visakhapatnam": "Andhra Pradesh",
    "Guntur": "Andhra Pradesh", "Nellore": "Andhra Pradesh", "Tirupati": "Andhra Pradesh",
    "Kurnool": "Andhra Pradesh", "Bengaluru": "Karnataka",
}
TIER_OF = {
    "Hyderabad": "Tier-1", "Bengaluru": "Tier-1",
    "Vijayawada": "Tier-2", "Visakhapatnam": "Tier-2", "Warangal": "Tier-2",
    "Guntur": "Tier-2", "Nellore": "Tier-2", "Tirupati": "Tier-2",
    "Karimnagar": "Tier-3", "Kurnool": "Tier-3",
}

CATEGORIES = [
    "OTC Medicines", "Prescription Medicines", "Wellness & Nutrition",
    "Personal Care", "Medical Devices", "Lab Tests",
]
CAT_WEIGHTS = [0.30, 0.22, 0.18, 0.14, 0.10, 0.06]

PRODUCTS = {
    "OTC Medicines": ["Paracetamol 500mg", "Cetirizine 10mg", "ORS Sachet", "Cough Syrup 100ml", "Antacid Tablets"],
    "Prescription Medicines": ["Metformin 500mg", "Amlodipine 5mg", "Atorvastatin 10mg", "Azithromycin 500mg", "Insulin Pen"],
    "Wellness & Nutrition": ["Multivitamin Tablets", "Whey Protein 1kg", "Fish Oil Capsules", "Immunity Booster Syrup", "Calcium + D3 Tablets"],
    "Personal Care": ["Sunscreen SPF50", "Hand Sanitizer 500ml", "Face Wash", "Antiseptic Liquid", "Baby Diaper Pack"],
    "Medical Devices": ["Digital BP Monitor", "Pulse Oximeter", "Glucometer Kit", "Nebulizer", "Thermometer"],
    "Lab Tests": ["Full Body Checkup", "Thyroid Profile", "Vitamin D Test", "HbA1c Test", "Lipid Profile"],
}

UNIT_PRICE = {
    "OTC Medicines": (40, 220), "Prescription Medicines": (90, 650),
    "Wellness & Nutrition": (250, 1400), "Personal Care": (80, 550),
    "Medical Devices": (350, 3200), "Lab Tests": (400, 1800),
}

MONTHS = [("2026-04", 30), ("2026-05", 31), ("2026-06", 30)]

REGION_BASE_WEIGHT = {
    "Hyderabad": 22, "Bengaluru": 16, "Vijayawada": 13, "Visakhapatnam": 12,
    "Warangal": 9, "Guntur": 9, "Nellore": 8, "Tirupati": 7, "Karimnagar": 4,
}
REGION_MONTH_MULTIPLIER = {
    "2026-04": defaultdict(lambda: 1.00),
    "2026-05": defaultdict(lambda: 1.00),
    "2026-06": defaultdict(lambda: 1.00),
}
REGION_MONTH_MULTIPLIER["2026-05"]["Visakhapatnam"] = 0.45
REGION_MONTH_MULTIPLIER["2026-06"]["Visakhapatnam"] = 0.70
REGION_MONTH_MULTIPLIER["2026-06"]["Hyderabad"] = 1.35

TARGET_ORDERS_PER_MONTH = 700

clean_rows = []
order_seq = 1
for month, ndays in MONTHS:
    weights = [REGION_BASE_WEIGHT[r] * REGION_MONTH_MULTIPLIER[month][r] for r in REGIONS_ACTIVE]
    for _ in range(TARGET_ORDERS_PER_MONTH):
        region = rng.choices(REGIONS_ACTIVE, weights=weights, k=1)[0]
        category = rng.choices(CATEGORIES, weights=CAT_WEIGHTS, k=1)[0]
        product = rng.choice(PRODUCTS[category])
        day = rng.randint(1, ndays)
        order_date = f"{month}-{day:02d}"
        qty = rng.randint(1, 5)
        lo, hi = UNIT_PRICE[category]
        unit_price = round(rng.uniform(lo, hi), 2)
        sales = round(unit_price * qty, 2)
        margin_pct = rng.uniform(0.08, 0.22)
        profit = round(sales * margin_pct, 2)
        clean_rows.append({
            "order_id": f"PE{order_seq:05d}",
            "order_date": order_date,
            "region": region,
            "category": category,
            "product": product,
            "quantity": qty,
            "sales_inr": sales,
            "profit_inr": profit,
        })
        order_seq += 1

working = [dict(r) for r in clean_rows]

missing_profit_idx = set(rng.sample(range(len(working)), 94))
missing_category_idx = set(rng.sample(range(len(working)), 48))
for i in missing_profit_idx:
    working[i]["profit_inr"] = ""
for i in missing_category_idx:
    working[i]["category"] = ""

messy_variants = {
    "Hyderabad": [" hyderabad", "HYDERABAD ", "Hyderabad"],
    "Bengaluru": ["bengaluru ", " BENGALURU", "Bengaluru"],
    "Vijayawada": ["vijayawada", " Vijayawada ", "VIJAYAWADA"],
}
messy_idx = rng.sample(range(len(working)), 161)
for i in messy_idx:
    r = working[i]["region"]
    if r in messy_variants:
        working[i]["region"] = rng.choice(messy_variants[r])

dup_source_idx = rng.sample(range(len(working)), 59)
duplicates = [dict(working[i]) for i in dup_source_idx]

raw_rows = working + duplicates
rng.shuffle(raw_rows)

with open("pharmeasy_orders_raw.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["order_id", "order_date", "region", "category", "product", "quantity", "sales_inr", "profit_inr"])
    w.writeheader()
    for r in raw_rows:
        w.writerow(r)

with open("regions_master.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["region", "state", "tier"])
    w.writeheader()
    for r in REGIONS_MASTER:
        w.writerow({"region": r, "state": STATE_OF[r], "tier": TIER_OF[r]})

assert len(raw_rows) == 2159, f"expected 2159 raw rows, got {len(raw_rows)}"
assert len(REGIONS_MASTER) == 10, f"expected 10 regions, got {len(REGIONS_MASTER)}"
print(f"Wrote pharmeasy_orders_raw.csv ({len(raw_rows)} rows) and regions_master.csv ({len(REGIONS_MASTER)} rows).")
