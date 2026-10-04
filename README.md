# PharmEasy Regional Pulse

## Regional Performance Analysis and Dashboard

This project analyzes regional sales performance using PharmEasy order data. It covers data generation, cleaning, validation, SQL-based metrics, significant-change flagging, draft reporting, human review, and an interactive dashboard.

## How to Run the Project

The project was developed using Google Colab and can also be run locally after cloning the repository.

### 1. Clone the repository

```bash
git clone https://github.com/nadellasriram/PharmEasy_Regional_Pulse.git
cd PharmEasy_Regional_Pulse
```

### 2. Install the required libraries

```bash
python -m pip install pandas streamlit plotly
```

### 3. Run the project scripts

Run the following commands from the project folder, in this order.

**Generate the dataset**

```bash
python generate_dataset.py
```

This generates the raw order dataset and the region master file.

**Clean and validate the data**

```bash
python clean_data.py
```

This cleans the raw data, removes duplicates, validates the records, and generates the data quality report.

**Build the SQLite database**

```bash
python build_db.py
```

This creates the database using the cleaned order data and region master file.

**Run SQL validation and queries**

```bash
python queries.py
```

This executes the SQL checks, calculates regional and monthly performance results, identifies significant changes, and saves the results in `state.json`.

**Generate the draft report and test the review gate**

```bash
python run_report_review.py
```

This loads the saved metrics, generates draft insight reports for flagged regions, and exercises the `approve`, `edit`, and `reject` review decisions. The test run appends entries to `audit_log.jsonl`.

The review decisions in this script are test cases. They demonstrate the review-gate behavior and do not represent actual manager approval.

**Launch the dashboard**

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal to explore the dashboard.

### Report generation and human review

The reporting workflow uses three modules:

- `metrics_engine.py` calculates percentage changes, flags significant regions, and saves or loads state.
- `draft_report.py` prepares a draft insight report for each flagged region.
- `review_gate.py` records a review decision, reviewer note, and whether external use is allowed.

The `run_report_review.py` script connects these modules for a reproducible demonstration of the workflow.

## Reviewer Cover Note

Guntur's sales increased by **122.19% from April to May 2026**, followed by a **28.11% decline from May to June**.

### Key Deliverables

- **Dashboard:** `app.py` — Interactive dashboard with sales, profit, order count, regional comparisons, category breakdowns, and monthly trends.
- **CII Executive Narrative:** Embedded in the dashboard, highlighting the key business situation, insights, and implications.
- **Recommendation Memo:** `memo.md` — Focused analysis of Guntur's sales change, with a recommendation for further investigation.
- **Review Memo:** `review_memo.md` — Checklist for validating the report before manager approval.
- **Presentation Storyline:** `presentation_storyline.md` — Executive and regional-manager narratives, including anticipated questions and responses.
- **Draft Report and Review Workflow:** `draft_report.py`, `review_gate.py`, and `run_report_review.py` — Draft generation and a testable human review process.

### Suggested Review Order

1. Open the dashboard and read the CII executive narrative.
2. Review the generated draft report and the flagged regional changes.
3. Read the recommendation memo and its supporting evidence.
4. Use the review memo to check data quality, metric accuracy, threshold application, regional coverage, and report wording.
5. Review the human review workflow and its audit log.
6. Read the presentation storyline and its Q&A section.

### Unverified Assumption

[MEDIUM] Any explanation involving demand, promotions or other external factors remains a hypothesis until verified using additional evidence.

## About This Project

I built this project as part of my Certification in Analytics and AI, with the objective of getting practical experience in data cleaning, SQL, Python automation, and dashboard development.

My professional experience has been mainly in recruitment, HR operations, and US payroll tax operations. In my current role as a Lead Specialist in payroll tax, I work with large volumes of data and understand how important accuracy, validation, and timely reporting are. I wanted to build on that experience and learn how to use data analytics to solve business problems.

For this capstone, I worked with PharmEasy order data to understand regional sales performance, identify changes over time, and present the findings in a dashboard that business users can explore.

## Project Objective

The main objective was to turn raw and inconsistent order data into a clean, validated dataset and use it to understand sales, profit, and order trends across regions.

I divided the work into four parts:

1. **Data Foundation and Validation:** Generate the dataset, clean inconsistent records, remove duplicates, and validate the results.
2. **SQL-Verified Metrics Engine and Flagging:** Use SQL and Python to calculate performance metrics and identify significant changes.
3. **Draft Report, Insight Narrative, and Human Review Gate:** Prepare a business-focused report and include a review process before recommendations are finalized.
4. **Dashboard and Stakeholder Presentation:** Build an interactive dashboard and prepare the key findings for executive and regional-manager discussions.

## Dataset Overview

The dataset initially contained 2,159 order rows. It included inconsistent region names and duplicate records, so I used Python to clean and validate it.

The key dataset checks were:

- Raw order rows: 2,159
- Duplicate rows removed: 59
- Clean order rows: 2,100
- Regions in the master file: 10
- Regions with recorded orders: 9
- Product categories: 6

Kurnool is included in the region master file but has no recorded orders in the cleaned order data.

## Tools and Technologies

During the project, I worked with:

- **Python:** For data generation, cleaning, calculations, and workflow automation.
- **pandas:** For handling and transforming the order data.
- **SQLite:** For storing the cleaned data and validating metrics through SQL queries.
- **Streamlit:** For creating the interactive dashboard.
- **Plotly:** For visualizing regional and monthly performance.
- **Google Colab:** For writing and running the Python scripts during development.
- **GitHub:** For organizing and sharing the project files.

The project does not require API keys or paid services.

## Project Files

| File | Description |
|---|---|
| `generate_dataset.py` | Generates the raw order data and region master file |
| `pharmeasy_orders_raw.csv` | Raw order dataset |
| `regions_master.csv` | Master list of regions and related details |
| `clean_data.py` | Cleans and validates the raw data |
| `pharmeasy_orders_clean.csv` | Cleaned order dataset |
| `data_quality_report.md` | Summary of data-quality checks and results |
| `build_db.py` | Creates the SQLite database |
| `pharmeasy.db` | Database containing the project data |
| `queries.py` | SQL queries and validation checks |
| `metrics_engine.py` | Calculates performance metrics and handles flagging |
| `state.json` | Saved state for monthly metrics and alert flags |
| `draft_report.py` | Generates the draft insight report |
| `run_report_review.py` | Runs report generation and demonstrates the review workflow |
| `review_gate.py` | Handles human review decisions and audit logging |
| `audit_log.jsonl` | Audit entries created by review decisions |
| `memo.md` | Business-focused recommendation memo |
| `review_memo.md` | Checklist for reviewing the report before approval |
| `reliability_checklist.md` | Checklist for reviewing reliability |
| `app.py` | Streamlit dashboard with Plotly charts |
| `presentation_storyline.md` | Executive and regional-manager presentation storyline |
| `README.md` | Project overview and instructions |

The review function creates or appends to `audit_log.jsonl` when a review decision is recorded. The committed log may contain test entries generated during validation.

## Key Findings

One of the changes I observed was in Guntur's monthly sales. Sales increased from ₹62,442.27 in April to ₹1,38,738.93 in May, which is a **122.19% increase**.

The number of orders also increased from 51 in April to 77 in May. In June, sales came down to ₹99,745.18 across 62 orders.

Hyderabad recorded the highest total sales in the dataset, at ₹7,47,583.99 across the three-month period.

These figures helped me identify where performance changed and where further investigation could be useful. The dataset shows the changes in sales and order volume, but it does not establish the business reasons behind them.

## Project Deliverables

I organized the final work around four main artifacts:

1. **Interactive dashboard (`app.py`):** Displays total sales, total profit, distinct orders, monthly sales trends, regional comparisons, and category contribution. The region filter allows users to explore the figures for individual regions.
2. **CII executive narrative:** Presents the key business situation, the main changes observed, and possible next steps. It is included at the top of the dashboard.
3. **Recommendation memo (`memo.md`):** Summarizes the Guntur finding and the proposed follow-up, with attention to the evidence and any remaining uncertainty.
4. **Presentation storyline (`presentation_storyline.md`):** Organizes the findings for executive and regional-manager discussions, including stakeholder questions and answers.

## What I Learned

Working on this project gave me an opportunity to connect the concepts I learned in the course with a practical business dataset. I got hands-on experience with cleaning inconsistent data, checking results using SQL, calculating performance changes, and presenting the output through a dashboard.

I also learned that identifying a change in the data is only one part of analysis. Understanding what caused that change requires further investigation and business context. This is something I want to continue improving as I work on more analytics projects.

## Submission

This project is maintained in a public GitHub repository as part of my Analytics and AI capstone. The repository contains the scripts, datasets, database, reports, and dashboard files used to complete the project.

**Repository:** https://github.com/nadellasriram/PharmEasy_Regional_Pulse
