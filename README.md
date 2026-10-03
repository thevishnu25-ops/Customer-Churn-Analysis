# Customer Churn Analysis

**Prepared by:** Vishnu Burusu

## Project Overview

This project analyzes customer churn for a
telecommunications/subscription-style dataset using Python and Power BI.
The objective is to identify patterns associated with customers leaving
the service and present the results through descriptive analysis,
visualizations, and an interactive dashboard.

## Tools Used

Python, Pandas, NumPy, Matplotlib, Seaborn, Power BI Desktop, Power
Query, and DAX.

## Dataset

The cleaned dataset contains **1,200 customers** and **23 columns**. It
includes demographic information, tenure, subscribed services, contract
type, billing information, payment method, monthly charges, total
charges, and churn status.

## Data Cleaning

The Python script: - checks shape, columns, data types, missing values,
duplicates, and unique values; - removes duplicate records; - trims text
fields; - converts tenure and charge fields to numeric values; - handles
missing numeric and categorical values; - creates `Tenure_Group`; -
creates `Churn_Flag` where 1 = churned and 0 = retained; - exports the
cleaned CSV for Power BI.

## Key KPIs

  KPI                               Result
  ------------------------- --------------
  Total Customers                    1,200
  Churned Customers                    501
  Retained Customers                   699
  Overall Churn Rate                41.75%
  Average Monthly Charges            78.87
  Average Total Charges           2,744.84
  Average Tenure              35.21 months

## Key Findings

1.  Month-to-month contracts have the highest churn rate at **59.51%**.
2.  Electronic check has the highest payment-method churn rate at
    **51.24%**.
3.  Fiber optic has the highest internet-service churn rate at
    **53.58%**.
4.  The 0-12 month tenure group has the highest churn rate at
    **60.95%**.
5.  Churned customers have higher average monthly charges (**84.88**)
    than retained customers (**74.57**).
6.  Gender churn rates are comparatively close, so stronger differences
    appear in contract, payment, service, and tenure categories.
7.  The correlation of monthly charges with churn is **0.22**, while
    tenure has a weak negative correlation of **-0.14**.

## Power BI Dashboard

Dashboard title: **Customer Churn & Retention Analytics Dashboard**

The dashboard includes: - KPI cards for total, churned, retained, churn
rate, average monthly charges, and average tenure; - churn
distribution; - churn rate by contract, internet service, and payment
method; - customer count by tenure group; - monthly charges by churn; -
customer distribution by contract and gender; - tenure vs monthly
charges scatter chart; - customer details table; - slicers for Gender,
Contract, Internet Service, Payment Method, Senior Citizen, and Churn.

## Core DAX Measures

``` dax
Total Customers =
DISTINCTCOUNT(Customer_Churn_Cleaned[Customer_ID])

Churned Customers =
CALCULATE(
    DISTINCTCOUNT(Customer_Churn_Cleaned[Customer_ID]),
    Customer_Churn_Cleaned[Churn] = "Yes"
)

Retained Customers =
CALCULATE(
    DISTINCTCOUNT(Customer_Churn_Cleaned[Customer_ID]),
    Customer_Churn_Cleaned[Churn] = "No"
)

Churn Rate % =
DIVIDE([Churned Customers], [Total Customers], 0)

Average Monthly Charges =
AVERAGE(Customer_Churn_Cleaned[Monthly_Charges])

Average Tenure =
AVERAGE(Customer_Churn_Cleaned[Tenure_Months])
```

## Folder Structure

``` text
Vishnu_Burusu_Customer_Churn_Analysis/
├── Dataset/
│   └── Vishnu_Burusu_Customer_Churn_Cleaned.csv
├── Python/
│   └── Vishnu_Burusu_Customer_Churn_Analysis.py
├── PowerBI/
│   └── Vishnu_Burusu_Customer_Churn_Analytics_Dashboard.pbix
├── Report/
│   └── Vishnu_Burusu_Customer_Churn_Project_Report.pdf
├── Visualizations/
│   └── 14 Python-generated charts
└── README.md
```

## How to Run

1.  Place the raw CSV in the same working directory as the Python script
    and name it `Customer_Churn_Raw.csv`.
2.  Install the required libraries: `pandas`, `numpy`, `matplotlib`, and
    `seaborn`.
3.  Run the Python script.
4.  The script creates `Customer_Churn_Cleaned.csv` and a
    `churn_visualizations` folder.
5.  Load the cleaned CSV into Power BI and build/use the dashboard.

## Conclusion

The analysis shows that churn is most strongly associated descriptively
with month-to-month contracts, electronic-check payments, fiber-optic
service, early tenure, and higher monthly charges. These findings
identify useful areas for deeper retention analysis. Association does
not by itself establish causation.
