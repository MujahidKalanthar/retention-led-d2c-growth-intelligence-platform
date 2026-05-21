import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Scenario Modeling",
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

st.title("🧠 Strategic Scenario Modeling Engine")

st.markdown("""
Executive simulation environment for evaluating future growth,
retention, profitability, and scaling scenarios.
""")

# =========================================
# SIDEBAR CONTROLS
# =========================================

st.sidebar.header("Scenario Inputs")

cac_increase = st.sidebar.slider(
    "CAC Increase (%)",
    min_value=0,
    max_value=50,
    value=15
)

repeat_rate_improvement = st.sidebar.slider(
    "Repeat Rate Improvement (%)",
    min_value=0,
    max_value=50,
    value=20
)

organic_growth = st.sidebar.slider(
    "Organic Traffic Growth (%)",
    min_value=0,
    max_value=60,
    value=25
)

gifting_growth = st.sidebar.slider(
    "Gifting Growth (%)",
    min_value=0,
    max_value=80,
    value=30
)

membership_growth = st.sidebar.slider(
    "Membership Adoption Growth (%)",
    min_value=0,
    max_value=60,
    value=20
)

# =========================================
# BASE METRICS
# =========================================

base_revenue = orders_df["order_value"].sum()

base_repeat_rate = (
    len(customers_df[customers_df["total_orders"] > 1])
    / len(customers_df)
)

base_ltv = customers_df["lifetime_value"].mean()

base_orders = len(orders_df)

# =========================================
# CAC MODEL
# =========================================

base_cac = 650

simulated_cac = (
    base_cac * (1 + cac_increase / 100)
)

# =========================================
# RETENTION MODEL
# =========================================

simulated_repeat_rate = (
    base_repeat_rate
    * (1 + repeat_rate_improvement / 100)
)

# =========================================
# ORGANIC GROWTH MODEL
# =========================================

organic_revenue_impact = (
    base_revenue * (organic_growth / 100)
)

# =========================================
# GIFTING MODEL
# =========================================

gifting_orders = len(
    orders_df[orders_df["gifting_order"] == True]
)

simulated_gifting_orders = (
    gifting_orders * (1 + gifting_growth / 100)
)

# =========================================
# MEMBERSHIP MODEL
# =========================================

membership_revenue_impact = (
    base_revenue * (membership_growth / 150)
)

# =========================================
# FINAL FORECAST
# =========================================

forecasted_revenue = (
    base_revenue
    + organic_revenue_impact
    + membership_revenue_impact
)

forecasted_ltv = (
    base_ltv
    * (1 + repeat_rate_improvement / 120)
)

forecasted_profitability = (
    forecasted_revenue
    * (simulated_repeat_rate)
    / simulated_cac
)

# =========================================
# KPI OUTPUTS
# =========================================

st.subheader("Scenario Forecast Output")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Forecasted Revenue",
    f"₹{round(forecasted_revenue):,}"
)

col2.metric(
    "Forecasted LTV",
    f"₹{round(forecasted_ltv,2)}"
)

col3.metric(
    "Simulated CAC",
    f"₹{round(simulated_cac,2)}"
)

col4.metric(
    "Projected Repeat Rate",
    f"{round(simulated_repeat_rate*100,2)}%"
)

# =========================================
# PROFITABILITY SCORE
# =========================================

st.subheader("Strategic Profitability Projection")

st.metric(
    "Profitability Efficiency Score",
    round(forecasted_profitability, 2)
)

# =========================================
# COMPARISON TABLE
# =========================================

comparison_df = pd.DataFrame({
    "Metric": [
        "Revenue",
        "LTV",
        "Repeat Rate",
        "CAC"
    ],
    "Current": [
        round(base_revenue, 2),
        round(base_ltv, 2),
        round(base_repeat_rate * 100, 2),
        round(base_cac, 2)
    ],
    "Forecasted": [
        round(forecasted_revenue, 2),
        round(forecasted_ltv, 2),
        round(simulated_repeat_rate * 100, 2),
        round(simulated_cac, 2)
    ]
})

st.subheader("Current vs Forecasted")

st.dataframe(comparison_df)

# =========================================
# VISUAL COMPARISON
# =========================================

fig = px.bar(
    comparison_df,
    x="Metric",
    y=["Current", "Forecasted"],
    barmode="group",
    title="Scenario Impact Analysis"
)

st.plotly_chart(fig, use_container_width=True)

# =========================================
# GIFTING INTELLIGENCE
# =========================================

st.subheader("Gifting & Virality Intelligence")

gift_df = pd.DataFrame({
    "Metric": [
        "Current Gifting Orders",
        "Projected Gifting Orders"
    ],
    "Value": [
        gifting_orders,
        round(simulated_gifting_orders)
    ]
})

fig_gift = px.bar(
    gift_df,
    x="Metric",
    y="Value",
    color="Metric",
    title="Gifting Growth Projection"
)

st.plotly_chart(fig_gift, use_container_width=True)

# =========================================
# STRATEGIC INSIGHTS
# =========================================

st.subheader("Executive Strategic Insights")

if repeat_rate_improvement > 15:
    st.success(
        "Retention improvements significantly increase LTV and reduce CAC recovery pressure."
    )

if organic_growth > 20:
    st.success(
        "Organic growth reduces dependency on paid acquisition and improves MER stability."
    )

if gifting_growth > 25:
    st.info(
        "Gifting behavior creates compounding organic acquisition loops."
    )

if cac_increase > 30:
    st.warning(
        "High CAC inflation may pressure profitability unless retention improves proportionally."
    )

# =========================================
# FOOTER
# =========================================

st.markdown("---")

st.caption("""
Scenario engine designed to model retention-led premium growth
strategies for D2C fragrance businesses.
""")