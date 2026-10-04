
import pandas as pd
import sqlite3

orders = pd.read_csv("pharmeasy_orders_clean.csv")
regions = pd.read_csv("regions_master.csv")

conn = sqlite3.connect("pharmeasy.db")

orders.to_sql("orders_clean", conn, if_exists="replace", index=False)
regions.to_sql("regions_master", conn, if_exists="replace", index=False)

print("orders_clean rows:", len(orders))
print("regions_master rows:", len(regions))

conn.close()

print("Saved: pharmeasy.db")
