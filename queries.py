
import sqlite3

from metrics_engine import (
    compute_percentage_change_v1,
    flag_significant_regions_v1
)

conn = sqlite3.connect("pharmeasy.db")

left_join = """
SELECT COUNT(*)
FROM regions_master r
LEFT JOIN orders_clean o
ON r.region = o.region
"""

inner_join = """
SELECT COUNT(*)
FROM regions_master r
INNER JOIN orders_clean o
ON r.region = o.region
"""

left_count = conn.execute(left_join).fetchone()[0]
inner_count = conn.execute(inner_join).fetchone()[0]

print("LEFT JOIN row count:", left_count)
print("INNER JOIN row count:", inner_count)
print("Delta:", left_count - inner_count)


duplicate_check = """
SELECT order_id, COUNT(*) AS duplicate_count
FROM orders_clean
GROUP BY order_id
HAVING COUNT(*) > 1
"""

duplicates = conn.execute(duplicate_check).fetchall()

print("Duplicate order_id rows:", duplicates)


count_check = """
SELECT
    r.region,
    COUNT(*) AS count_star,
    COUNT(o.order_id) AS count_order_id
FROM regions_master r
LEFT JOIN orders_clean o
ON r.region = o.region
GROUP BY r.region
ORDER BY r.region
"""

count_results = conn.execute(count_check).fetchall()

print("COUNT(*) vs COUNT(order_id):")
for row in count_results:
    print(row)


region_counts_query = """
SELECT
    r.region,
    COUNT(o.order_id) AS order_count
FROM regions_master r
LEFT JOIN orders_clean o
ON r.region = o.region
GROUP BY r.region
ORDER BY order_count ASC
"""

region_counts = conn.execute(region_counts_query).fetchall()

print("Per-region order counts:")
for row in region_counts:
    print(row)


region_month_sales_query = """
SELECT
    region,
    substr(order_date, 1, 7) AS month,
    SUM(sales_inr) AS total_sales
FROM orders_clean
GROUP BY region, substr(order_date, 1, 7)
ORDER BY region, month
"""

region_month_sales = conn.execute(region_month_sales_query).fetchall()

print("Region x month sales:")
for row in region_month_sales:
    print(row)


sales_by_region = {}

for region, month, sales in region_month_sales:
    if region not in sales_by_region:
        sales_by_region[region] = {}

    sales_by_region[region][month] = sales


print("MoM sales changes:")

april_to_may_changes = {}
may_to_june_changes = {}

for region in sales_by_region:
    april_sales = sales_by_region[region]["2026-04"]
    may_sales = sales_by_region[region]["2026-05"]
    june_sales = sales_by_region[region]["2026-06"]

    april_to_may = compute_percentage_change_v1(
        may_sales, april_sales
    )

    may_to_june = compute_percentage_change_v1(
        june_sales, may_sales
    )

    april_to_may_changes[region] = april_to_may
    may_to_june_changes[region] = may_to_june

    print(
        region,
        "Apr->May:", round(april_to_may, 2),
        "May->Jun:", round(may_to_june, 2)
    )


april_to_may_flags = flag_significant_regions_v1(
    april_to_may_changes
)

may_to_june_flags = flag_significant_regions_v1(
    may_to_june_changes
)

print("\nSignificant regions (Apr->May):")
print(april_to_may_flags)

print("\nSignificant regions (May->Jun):")
print(may_to_june_flags)

from metrics_engine import save_state_v1

current_state = {
    "last_month": "2026-06",
    "monthly_sales": sales_by_region,
    "april_to_may_changes": april_to_may_changes,
    "may_to_june_changes": may_to_june_changes,
    "april_to_may_flags": april_to_may_flags,
    "may_to_june_flags": may_to_june_flags
}

save_state_v1(current_state)

print("Saved current state:")
print(current_state)

conn.close()
