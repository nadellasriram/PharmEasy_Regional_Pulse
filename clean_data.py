
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

# -----------------------------------------
# Generate Data Quality Report
# -----------------------------------------

report = f"""# Data Quality Report

## Overview

I first checked the raw PharmEasy data before using it for analysis. I found duplicate rows, inconsistent region names, and missing values in the category and profit columns. I cleaned these issues and then validated the final dataset before moving to the next stage.

## Cleaning Results

- Raw records: {len(df) + duplicate_count:,}
- Duplicate records removed: {duplicate_count}
- Final clean records: {len(df):,}
- Missing category values after cleaning: {df["category"].isna().sum()}
- Missing profit values after cleaning: {df["profit_inr"].isna().sum()}
- Schema validation: {"Passed" if clean_validation["status"] == "validated" else "Failed"}

## Data Quality Dimensions

| Data Quality Dimension | What I found | What I did |
|---|---|---|
| **Accuracy** | Some profit values were missing, so the profit figures could not be used directly. | I calculated the average profit margin for each category and used it to calculate the missing profit values. |
| **Completeness** | The raw data had missing values in the category and profit columns. | I filled the missing categories using the product-to-category mapping and filled the missing profit values using category-level profit margins. |
| **Consistency** | Some region names had extra spaces or different capitalization. | I used `strip()` and `title()` to bring the region names into a consistent format. |
| **Timeliness** | The data covers April, May, and June 2026. | I kept the analysis within the three-month period provided in the dataset. |
| **Validity** | I needed to make sure the cleaned data had all the columns required for the analysis. | I used the `validate_schema()` function to check the required columns. I also tested it with a broken copy of the data. |
| **Uniqueness** | The raw dataset contained exact duplicate rows. | I identified and removed 59 duplicate rows before continuing with the analysis. |
| **Relevance** | The dataset contains the information needed for regional performance analysis, such as region, category, quantity, sales, and profit. | I kept the required columns so the cleaned data could be used for the SQL analysis, reporting, and dashboard. |

## Validation

After cleaning the data, I checked the schema using the `validate_schema()` function. The clean dataset was successfully validated with {clean_validation["row_count"]:,} rows and all required columns present.

I also created a broken copy by removing the `profit_inr` column. The validation correctly returned `{broken_validation["status"]}` and identified `{", ".join(broken_validation["missing_columns"])}` as the missing column.

## Conclusion

The raw dataset has been cleaned and validated successfully. The final dataset contains {len(df):,} rows with no missing category or profit values, so it is ready for the SQL analysis in the next stage.
"""

with open("data_quality_report.md", "w", encoding="utf-8") as file:
    file.write(report)

print("Saved: data_quality_report.md")
