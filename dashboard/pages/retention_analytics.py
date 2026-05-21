import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Retention Analytics",
    layout="wide"
)

# =========================================
# LOAD DATA
# =========================================

customers_df = pd.read_csv("data/synthetic/customers.csv")
orders_df = pd.read_csv("data/synthetic/orders.csv")

# =========================================
# HEADER
# =========================================

st.title("🔁 Retention & Cohort Analytics")

st.markdown("""
Analyze customer retention behavior, repeat purchase patterns,
and lifecycle progression across cohorts.
""")

# =========================================
# PREPARE DATES
# =========================================

customers_df["acquisition_date"] = pd.to_datetime(
    customers_df["acquisition_date"]
)

customers_df["cohort_month"] = (
    customers_df["acquisition_date"]
    .dt.to_period("M")
    .astype(str)
)

# =========================================
# COHORT ANALYSIS
# =========================================

cohort_analysis = (
    customers_df.groupby("cohort_month")
    .agg({
        "customer_id": "count",
        "lifetime_value": "mean",
        "repeat_purchase_rate": "mean",
        "churn_risk_score": "mean"
    })
    .reset_index()
)

cohort_analysis.columns = [
    "cohort_month",
    "customers_acquired",
    "avg_ltv",
    "avg_repeat_rate",
    "avg_churn_risk"
]

# =========================================
# KPI ROW
# =========================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Repeat Rate",
    f"{round(cohort_analysis['avg_repeat_rate'].mean()*100,2)}%"
)

col2.metric(
    "Average Cohort LTV",
    f"₹{round(cohort_analysis['avg_ltv'].mean(),2)}"
)

col3.metric(
    "Average Churn Risk",
    round(cohort_analysis["avg_churn_risk"].mean(), 2)
)

# =========================================
# COHORT ACQUISITION TREND
# =========================================

st.subheader("Monthly Customer Acquisition Cohorts")

fig_cohort = px.line(
    cohort_analysis,
    x="cohort_month",
    y="customers_acquired",
    markers=True,
    title="Customers Acquired by Cohort"
)

st.plotly_chart(fig_cohort, use_container_width=True)

# =========================================
# LTV BY COHORT
# =========================================

st.subheader("Average Lifetime Value by Cohort")

fig_ltv = px.bar(
    cohort_analysis,
    x="cohort_month",
    y="avg_ltv",
    color="avg_ltv",
    title="Cohort LTV Trends"
)

st.plotly_chart(fig_ltv, use_container_width=True)

# =========================================
# REPEAT RATE ANALYSIS
# =========================================

st.subheader("Repeat Purchase Rate Trends")

fig_repeat = px.line(
    cohort_analysis,
    x="cohort_month",
    y="avg_repeat_rate",
    markers=True,
    title="Repeat Purchase Rate by Cohort"
)

st.plotly_chart(fig_repeat, use_container_width=True)

# =========================================
# CHURN RISK ANALYSIS
# =========================================

st.subheader("Cohort Churn Risk")

fig_churn = px.area(
    cohort_analysis,
    x="cohort_month",
    y="avg_churn_risk",
    title="Churn Risk Across Cohorts"
)

st.plotly_chart(fig_churn, use_container_width=True)

# =========================================
# SEGMENT RETENTION
# =========================================

st.subheader("Retention Performance by Customer Segment")

segment_retention = (
    customers_df.groupby("customer_segment")
    .agg({
        "repeat_purchase_rate": "mean",
        "lifetime_value": "mean",
        "churn_risk_score": "mean"
    })
    .reset_index()
)

fig_segment = px.scatter(
    segment_retention,
    x="repeat_purchase_rate",
    y="lifetime_value",
    size="churn_risk_score",
    color="customer_segment",
    title="Segment Retention Intelligence"
)

st.plotly_chart(fig_segment, use_container_width=True)

# =========================================
# FOOTER INSIGHTS
# =========================================

st.markdown("---")

st.info("""
Key Strategic Insight:
Premium Loyalists and Fragrance Collectors drive disproportionately
higher LTV and repeat rates, validating the case strategy’s emphasis
on retention-led premium growth over discount-led acquisition.
""")