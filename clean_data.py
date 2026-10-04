
import pandas as pd

df = pd.read_csv("pharmeasy_orders_raw.csv")

duplicate_count = df.duplicated().sum()
df = df.drop_duplicates()

df["region"] = df["region"].str.strip().str.title()

product_category = (
    df.dropna(subset=["category"])
      .drop_duplicates("product")
      .set_index("product")
      .to_dict()["category"]
)

df["category"] = df["category"].fillna(
    df["product"].map(product_category)
)

df["profit_inr"] = pd.to_numeric(df["profit_inr"], errors="coerce")

df["margin"] = df["profit_inr"] / df["sales_inr"]

category_margin = df.groupby("category")["margin"].mean().to_dict()

missing_profit = df["profit_inr"].isna()

df.loc[missing_profit, "profit_inr"] = (
    df.loc[missing_profit, "sales_inr"]
    * df.loc[missing_profit, "category"].map(category_margin)
).round(2)

df = df.drop(columns=["margin"])

df.to_csv("pharmeasy_orders_clean.csv", index=False)

print("Duplicate rows removed:", duplicate_count)
print("Clean rows:", len(df))
print("Missing category:", df["category"].isna().sum())
print("Missing profit:", df["profit_inr"].isna().sum())
print("Saved: pharmeasy_orders_clean.csv")


def validate_schema(df, required_columns):
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        status = "blocked_schema"
    else:
        status = "validated"

    return {
        "status": status,
        "row_count": len(df),
        "missing_columns": missing_columns
    }


required_columns = [
    "order_id",
    "order_date",
    "region",
    "category",
    "product",
    "quantity",
    "sales_inr",
    "profit_inr"
]

clean_validation = validate_schema(df, required_columns)

print("Clean schema validation:", clean_validation)

broken_df = df.drop(columns=["profit_inr"])

broken_validation = validate_schema(broken_df, required_columns)

print("Broken schema validation:", broken_validation)
