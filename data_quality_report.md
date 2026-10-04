# Data Quality Report

## Overview

I first checked the raw PharmEasy data before using it for analysis. I found duplicate rows, inconsistent region names, and missing values in the category and profit columns. I cleaned these issues and then validated the final dataset before moving to the next stage.

## Cleaning Results

- Raw records: 2,159
- Duplicate records removed: 59
- Final clean records: 2,100
- Missing category values after cleaning: 0
- Missing profit values after cleaning: 0
- Schema validation: Passed

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

After cleaning the data, I checked the schema using the `validate_schema()` function. The clean dataset was successfully validated with 2,100 rows and all required columns present.

I also created a broken copy by removing the `profit_inr` column. The validation correctly returned `blocked_schema` and identified `profit_inr` as the missing column.

## Conclusion

The raw dataset has been cleaned and validated successfully. The final dataset contains 2,100 rows with no missing category or profit values, so it is ready for the SQL analysis in the next stage.
