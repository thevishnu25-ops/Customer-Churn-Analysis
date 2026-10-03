# ============================================================
# CUSTOMER CHURN ANALYSIS - COMPLETE BEGINNER PROJECT
# Based on the supplied project brief
# ============================================================

# Install once in terminal if needed:
# pip install pandas numpy matplotlib seaborn

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# 1. SETTINGS
# -----------------------------
pd.set_option("display.max_columns", None)
sns.set_theme(style="whitegrid")

INPUT_FILE = "Customer_Churn_Raw.csv"
CLEANED_FILE = "Customer_Churn_Cleaned.csv"
OUTPUT_FOLDER = "churn_visualizations"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -----------------------------
# 2. LOAD DATA
# -----------------------------
df = pd.read_csv(INPUT_FILE)

print("\nFIRST 5 RECORDS")
print(df.head())

print("\nLAST 5 RECORDS")
print(df.tail())

print("\nDATASET SHAPE")
print(df.shape)

print("\nCOLUMN NAMES")
print(df.columns.tolist())

# -----------------------------
# 3. DATA EXPLORATION
# -----------------------------
print("\nDATA TYPES")
print(df.dtypes)

print("\nSTATISTICAL SUMMARY")
print(df.describe(include="all"))

print("\nMISSING VALUES BEFORE CLEANING")
print(df.isnull().sum())

print("\nDUPLICATE RECORDS")
print(df.duplicated().sum())

print("\nUNIQUE VALUES PER COLUMN")
for column in df.columns:
    print(f"\n{column}:")
    print(df[column].unique())

# -----------------------------
# 4. DATA CLEANING
# -----------------------------
# Remove exact duplicate records
df = df.drop_duplicates().copy()

# Remove accidental spaces from text columns
text_columns = df.select_dtypes(include="object").columns
for column in text_columns:
    df[column] = df[column].str.strip()

# Convert numeric columns safely
df["Tenure_Months"] = pd.to_numeric(df["Tenure_Months"], errors="coerce")
df["Monthly_Charges"] = pd.to_numeric(df["Monthly_Charges"], errors="coerce")
df["Total_Charges"] = pd.to_numeric(df["Total_Charges"], errors="coerce")

# Handle missing numeric values
df["Tenure_Months"] = df["Tenure_Months"].fillna(df["Tenure_Months"].median())
df["Monthly_Charges"] = df["Monthly_Charges"].fillna(df["Monthly_Charges"].median())
df["Total_Charges"] = df["Total_Charges"].fillna(df["Monthly_Charges"] * df["Tenure_Months"])

# Handle missing categorical values if any
for column in text_columns:
    if df[column].isnull().any():
        mode_value = df[column].mode()[0]
        df[column] = df[column].fillna(mode_value)

# Create tenure groups
tenure_bins = [-1, 12, 24, 48, 60, np.inf]
tenure_labels = ["0-12 Months", "13-24 Months", "25-48 Months",
                 "49-60 Months", "61+ Months"]

df["Tenure_Group"] = pd.cut(
    df["Tenure_Months"],
    bins=tenure_bins,
    labels=tenure_labels
)

# Helpful numeric churn flag: 1 = churned, 0 = retained
df["Churn_Flag"] = np.where(df["Churn"].str.lower() == "yes", 1, 0)

print("\nMISSING VALUES AFTER CLEANING")
print(df.isnull().sum())

print("\nDUPLICATES AFTER CLEANING")
print(df.duplicated().sum())

print("\nCLEANED DATA TYPES")
print(df.dtypes)

print("\nCLEANED DATA PREVIEW")
print(df.head())

# Save cleaned dataset for Power BI
df.to_csv(CLEANED_FILE, index=False)
print(f"\nCleaned dataset saved as: {CLEANED_FILE}")

# -----------------------------
# 5. CORE DATA ANALYSIS
# -----------------------------
total_customers = df["Customer_ID"].nunique()
churned_customers = df.loc[df["Churn"] == "Yes", "Customer_ID"].nunique()
retained_customers = df.loc[df["Churn"] == "No", "Customer_ID"].nunique()
churn_rate = (churned_customers / total_customers) * 100
avg_monthly_charges = df["Monthly_Charges"].mean()
avg_total_charges = df["Total_Charges"].mean()
avg_tenure = df["Tenure_Months"].mean()

print("\n========== KPI SUMMARY ==========")
print("Total Customers:", total_customers)
print("Churned Customers:", churned_customers)
print("Retained Customers:", retained_customers)
print(f"Overall Churn Rate: {churn_rate:.2f}%")
print(f"Average Monthly Charges: {avg_monthly_charges:.2f}")
print(f"Average Total Charges: {avg_total_charges:.2f}")
print(f"Average Customer Tenure: {avg_tenure:.2f} months")

print("\nCUSTOMERS BY GENDER")
print(df["Gender"].value_counts())

print("\nCUSTOMERS BY CONTRACT TYPE")
print(df["Contract"].value_counts())

print("\nCUSTOMERS BY INTERNET SERVICE")
print(df["Internet_Service"].value_counts())

print("\nCUSTOMERS BY PAYMENT METHOD")
print(df["Payment_Method"].value_counts())

# Reusable churn-rate function
def churn_rate_by(column):
    result = (
        df.groupby(column, observed=False)["Churn_Flag"]
          .agg(Total_Customers="count", Churned_Customers="sum", Churn_Rate="mean")
          .reset_index()
    )
    result["Churn_Rate"] = result["Churn_Rate"] * 100
    return result.sort_values("Churn_Rate", ascending=False)

print("\nCHURN RATE BY GENDER")
print(churn_rate_by("Gender"))

print("\nCHURN RATE BY CONTRACT TYPE")
print(churn_rate_by("Contract"))

print("\nCHURN RATE BY INTERNET SERVICE")
print(churn_rate_by("Internet_Service"))

print("\nCHURN RATE BY PAYMENT METHOD")
print(churn_rate_by("Payment_Method"))

print("\nCHURN RATE BY SENIOR CITIZEN STATUS")
print(churn_rate_by("Senior_Citizen"))

print("\nCHURN RATE BY TENURE GROUP")
print(churn_rate_by("Tenure_Group"))

print("\nMONTHLY CHARGES: CHURNED VS RETAINED")
print(df.groupby("Churn")["Monthly_Charges"].agg(["count", "mean", "median", "min", "max"]))

print("\nTENURE: CHURNED VS RETAINED")
print(df.groupby("Churn")["Tenure_Months"].agg(["count", "mean", "median", "min", "max"]))

print("\nTOP 10 CUSTOMERS BY TOTAL CHARGES")
top10 = df.nlargest(10, "Total_Charges")[
    ["Customer_ID", "Contract", "Internet_Service", "Monthly_Charges",
     "Total_Charges", "Tenure_Months", "Churn"]
]
print(top10)

# Segment analysis: Contract + Internet Service + Payment Method
segment_analysis = (
    df.groupby(["Contract", "Internet_Service", "Payment_Method"], observed=False)
      .agg(
          Total_Customers=("Customer_ID", "nunique"),
          Churned_Customers=("Churn_Flag", "sum"),
          Average_Monthly_Charges=("Monthly_Charges", "mean"),
          Average_Tenure=("Tenure_Months", "mean")
      )
      .reset_index()
)

segment_analysis["Churn_Rate"] = np.where(
    segment_analysis["Total_Customers"] > 0,
    segment_analysis["Churned_Customers"] / segment_analysis["Total_Customers"] * 100,
    0
)

segment_analysis = segment_analysis[
    segment_analysis["Total_Customers"] >= 10
].sort_values("Churn_Rate", ascending=False)

print("\nHIGHER-CHURN CUSTOMER SEGMENTS (minimum 10 customers)")
print(segment_analysis.head(10))

# Factor summary
factor_summary = pd.concat([
    churn_rate_by("Contract").assign(Factor="Contract").rename(columns={"Contract": "Category"}),
    churn_rate_by("Internet_Service").assign(Factor="Internet Service").rename(columns={"Internet_Service": "Category"}),
    churn_rate_by("Payment_Method").assign(Factor="Payment Method").rename(columns={"Payment_Method": "Category"}),
    churn_rate_by("Tenure_Group").assign(Factor="Tenure Group").rename(columns={"Tenure_Group": "Category"}),
], ignore_index=True)

print("\nMAJOR FACTORS / CATEGORIES ASSOCIATED WITH CHURN")
print(factor_summary[["Factor", "Category", "Total_Customers",
                      "Churned_Customers", "Churn_Rate"]]
      .sort_values("Churn_Rate", ascending=False)
      .head(15))

# -----------------------------
# 6. VISUALIZATIONS
# -----------------------------
def save_show(filename):
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, filename), dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

# 1. Churn Distribution - Pie Chart
churn_counts = df["Churn"].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(churn_counts.values, labels=churn_counts.index, autopct="%1.1f%%", startangle=90)
plt.title("Churn Distribution")
save_show("01_churn_distribution.png")

# 2. Customer Distribution by Contract - Bar Chart
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="Contract", order=df["Contract"].value_counts().index)
plt.title("Customer Distribution by Contract")
plt.xlabel("Contract")
plt.ylabel("Customer Count")
save_show("02_customer_distribution_by_contract.png")

# 3. Churn by Contract - Bar Chart
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="Contract", hue="Churn")
plt.title("Churn by Contract")
plt.xlabel("Contract")
plt.ylabel("Customer Count")
save_show("03_churn_by_contract.png")

# 4. Churn by Gender - Bar Chart
plt.figure(figsize=(7, 5))
sns.countplot(data=df, x="Gender", hue="Churn")
plt.title("Churn by Gender")
plt.xlabel("Gender")
plt.ylabel("Customer Count")
save_show("04_churn_by_gender.png")

# 5. Churn by Internet Service - Bar Chart
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="Internet_Service", hue="Churn")
plt.title("Churn by Internet Service")
plt.xlabel("Internet Service")
plt.ylabel("Customer Count")
save_show("05_churn_by_internet_service.png")

# 6. Churn by Payment Method - Bar Chart
plt.figure(figsize=(11, 6))
sns.countplot(data=df, y="Payment_Method", hue="Churn")
plt.title("Churn by Payment Method")
plt.xlabel("Customer Count")
plt.ylabel("Payment Method")
save_show("06_churn_by_payment_method.png")

# 7. Tenure Distribution - Histogram
plt.figure(figsize=(8, 5))
sns.histplot(data=df, x="Tenure_Months", bins=20, kde=True)
plt.title("Tenure Distribution")
plt.xlabel("Tenure (Months)")
plt.ylabel("Customer Count")
save_show("07_tenure_distribution.png")

# 8. Monthly Charges Distribution - Histogram
plt.figure(figsize=(8, 5))
sns.histplot(data=df, x="Monthly_Charges", bins=20, kde=True)
plt.title("Monthly Charges Distribution")
plt.xlabel("Monthly Charges")
plt.ylabel("Customer Count")
save_show("08_monthly_charges_distribution.png")

# 9. Tenure vs Monthly Charges - Scatter Plot
plt.figure(figsize=(9, 6))
sns.scatterplot(data=df, x="Tenure_Months", y="Monthly_Charges", hue="Churn", alpha=0.65)
plt.title("Tenure vs Monthly Charges")
plt.xlabel("Tenure (Months)")
plt.ylabel("Monthly Charges")
save_show("09_tenure_vs_monthly_charges.png")

# 10. Monthly Charges by Churn - Box Plot
plt.figure(figsize=(7, 5))
sns.boxplot(data=df, x="Churn", y="Monthly_Charges")
plt.title("Monthly Charges by Churn")
plt.xlabel("Churn")
plt.ylabel("Monthly Charges")
save_show("10_monthly_charges_by_churn.png")

# 11. Total Charges by Churn - Box Plot
plt.figure(figsize=(7, 5))
sns.boxplot(data=df, x="Churn", y="Total_Charges")
plt.title("Total Charges by Churn")
plt.xlabel("Churn")
plt.ylabel("Total Charges")
save_show("11_total_charges_by_churn.png")

# 12. Churn Rate by Tenure Group - Bar Chart
tenure_churn = churn_rate_by("Tenure_Group")
plt.figure(figsize=(9, 5))
sns.barplot(data=tenure_churn, x="Tenure_Group", y="Churn_Rate")
plt.title("Churn Rate by Tenure Group")
plt.xlabel("Tenure Group")
plt.ylabel("Churn Rate (%)")
plt.xticks(rotation=20)
save_show("12_churn_rate_by_tenure_group.png")

# 13. Service Usage - Count Plot
service_columns = [
    "Phone_Service", "Multiple_Lines", "Online_Security", "Online_Backup",
    "Device_Protection", "Tech_Support", "Streaming_TV", "Streaming_Movies"
]

service_long = df[service_columns].melt(var_name="Service", value_name="Status")
plt.figure(figsize=(12, 7))
sns.countplot(data=service_long, y="Service", hue="Status")
plt.title("Service Usage")
plt.xlabel("Customer Count")
plt.ylabel("Service")
save_show("13_service_usage.png")

# 14. Correlation Heatmap
corr_df = df[["Tenure_Months", "Monthly_Charges", "Total_Charges", "Churn_Flag"]].corr()
plt.figure(figsize=(7, 5))
sns.heatmap(corr_df, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation Heatmap")
save_show("14_correlation_heatmap.png")

print("\nAll analysis is complete.")
print(f"Charts were saved in the folder: {OUTPUT_FOLDER}")
print(f"Use {CLEANED_FILE} as the main dataset in Power BI.")
