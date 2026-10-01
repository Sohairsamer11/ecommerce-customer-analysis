🛒 E-commerce Customer Analysis | Python & Streamlit
An end-to-end customer analytics project: data cleaning and exploratory analysis in Python, followed by an interactive Streamlit dashboard that turns the findings into something a business team can explore.

[View the Interactive Streamlit Dashboard](https://ecommerce-customer-analysis-sohair.streamlit.app/)

📌 Project Overview

An e-commerce business wants to understand who its customers are, how they behave, and which customers create the most value. This project analyzes a dataset of 10,000 customers (23 features covering demographics, purchasing behavior, marketing engagement, and customer experience) to answer questions such as:

Who are our customers by age, gender, income, and location?
How do repeat customers differ from non-repeat customers?
Which customers have low or negative lifetime value, and why?
Do marketing engagement and customer service activity translate into conversions and satisfaction?
🎯 Objectives
Assess data quality and clean the dataset with defensible, documented decisions.
Explore customer demographics, behavior, engagement, and experience.
Identify the factors associated with customer value (CLV).
Deliver the results as an interactive dashboard for non-technical users.
📂 Repository Structure
ecommerce-customer-analysis/
├── app.py                                   # Streamlit dashboard
├── Ecommerce_Customer_Analysis_Final.ipynb  # Cleaning + EDA notebook
├── ecommerce_customer_data.csv              # Raw dataset (10,000 rows × 23 columns)
├── requirements.txt                         # Python dependencies
└── README.md
## 🗂️ Dataset

| Group | Columns |
|---|---|
| **Identity** | `CustomerID`, `RegistrationDate` |
| **Demographics** | `Age`, `Gender`, `IncomeLevel`, `Country`, `City` |
| **Purchasing** | `TotalPurchases`, `AverageOrderValue`, `CustomerLifetimeValue`, `FavoriteCategory`, `SecondFavoriteCategory` |
| **Engagement** | `EmailEngagementRate`, `SocialMediaEngagementRate`, `MobileAppUsage` |
| **Customer experience** | `CustomerServiceInteractions`, `AverageSatisfactionScore` |
| **Conversion** | `EmailConversionRate`, `SocialMediaConversionRate`, `SearchEngineConversionRate` |
| **Status flags** | `RepeatCustomer`, `PremiumMember`, `HasReturnedItems` |
## 🧹 Data Cleaning

The raw data was intentionally messy. Every cleaning decision was based on what the data showed:

| Issue found | Action taken |
|---|---|
| Inconsistent labels (`M`/`F` for Gender, `H`/`L` for IncomeLevel) | Standardized to `Male`/`Female` and `High`/`Low` |
| 89 negative ages and 28 zero ages (impossible values) | Treated as missing, then imputed with the median |
| Missing values in all 23 columns (≈5% in most; up to 26% in Gender, IncomeLevel, MobileAppUsage) | Numeric → median imputation. Categorical → kept as an explicit `Unknown` category instead of guessing |
| 492 missing `CustomerID` values flagged as "duplicates" | Verified that **no real duplicates exist**: all non-missing IDs are unique |
| `RegistrationDate` stored as text | Converted to `datetime` |
| Extreme `AverageOrderValue` outliers (up to ≈ 51,810) | **Kept** and handled by using the median and a capped view for charts |
| 936 customers (9.36%) with negative `CustomerLifetimeValue` | **Kept and investigated** rather than silently deleted, because the CLV formula is not documented |

## 🔍 Key Findings

1. **Repeat customers are far more active.** They average about **5.5 purchases** versus **under 1** for non-repeat customers, and their median CLV is roughly **4–5× higher**.
2. **9.36% of customers have negative CLV**, and the problem is concentrated among non-repeat customers: **31.07%** of non-repeat customers have negative CLV compared with **6.69%** of repeat customers. Return behavior does *not* explain it (28.6% vs 28.3% return rate in both groups).
3. **Order value is highly right-skewed.** The mean AOV (≈ 182) is more than 3× the median (≈ 54.5), so the median is the honest measure of a typical order.
4. **Engagement does not translate into conversion.** The correlation between email engagement and email conversion is ≈ **−0.001**, and ≈ **−0.017** for social media.
5. **More support contact ≠ lower satisfaction.** Customer service interactions and satisfaction score are essentially uncorrelated (≈ 0.002).
6. **The customer base is broadly balanced** across countries, cities, categories, and income levels, so no single market or segment dominates.
7. **Customer status:** about **89%** of customers with known status are repeat customers, **≈ 20%** are premium members, and **≈ 30%** have returned items.

## 📊 Dashboard Features

The Streamlit app lets users filter the whole dashboard by **Country, Gender, Income Level, and Customer Type** and see the results update instantly.

- **KPIs:** total customers, average order value, total purchases, average satisfaction
- **Customer analysis:** gender, age groups, purchase behavior, engagement, mobile app usage, customer experience
- **Geographic analysis:** customers by country and by income level
- **Customer segmentation:** repeat vs non-repeat and premium vs non-premium
- **Business insight cards:** repeat rate, premium rate, return rate, and average CLV for the current filter selection

## 🚀 Run It Locally

```bash
# 1. Clone the repository
git clone https://github.com/Sohairsamer11/ecommerce-customer-analysis.git
cd ecommerce-customer-analysis

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the dashboard
streamlit run app.py
```

To explore the analysis itself, open `Ecommerce_Customer_Analysis_Final.ipynb` in Jupyter. Note that the notebook uses `statsmodels` for the OLS trendlines, so run `pip install statsmodels jupyter` first.

## 🛠️ Tech Stack

- **Python**: pandas, NumPy
- **Visualization**: Plotly Express / Graph Objects
- **Dashboard**: Streamlit (deployed on Streamlit Community Cloud)

## ⚠️ Limitations & Next Steps

- The CLV formula is not documented, so negative values are flagged rather than corrected. Confirming the formula with the data owner is the first step.
- Median imputation keeps all 10,000 rows but can flatten differences between groups. Comparisons on categorical flags (repeat, premium) used known values only, but the numeric comparisons would benefit from a re-run on non-imputed data.
- Possible extensions: RFM segmentation, churn prediction, cohort analysis by `RegistrationDate`, and statistical significance tests for group comparisons.

## 👩‍💻 Author

**Sohair Samer**: Data Analyst

