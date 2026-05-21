import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Pricing Simulator",
    layout="wide"
)

# =========================================
# LOAD DATA
# =========================================

orders_df = pd.read_csv("data/synthetic/orders.csv")
customers_df = pd.read_csv("data/synthetic/customers.csv")

# =========================================
# HEADER
# =========================================

st.title("💰 Pricing & Margin Intelligence Simulator")

st.markdown("""
Interactive simulation engine for evaluating pricing strategy,
discount dependency, premiumization, and profitability impact.
""")

# =========================================
# SIDEBAR CONTROLS
# =========================================

st.sidebar.header("Simulation Controls")

discount_reduction = st.sidebar.slider(
    "Reduce Discounts (%)",
    min_value=0,
    max_value=40,
    value=10
)

aov_growth = st.sidebar.slider(
    "Increase AOV (%)",
    min_value=0,
    max_value=50,
    value=15
)

premium_adoption = st.sidebar.slider(
    "Premium Set Adoption (%)",
    min_value=0,
    max_value=60,
    value=20
)

membership_growth = st.sidebar.slider(
    "Membership Growth (%)",
    min_value=0,
    max_value=50,
    value=15
)

# =========================================
# BASE METRICS
# =========================================

base_revenue = orders_df["order_value"].sum()

base_margin = orders_df["gross_margin"].mean()

base_discount = orders_df["discount_percent"].mean()

base_aov = orders_df["order_value"].mean()

# =========================================
# SIMULATION LOGIC
# =========================================

simulated_discount = (
    base_discount * (1 - discount_reduction / 100)
)

simulated_aov = (
    base_aov * (1 + aov_growth / 100)
)

simulated_revenue = (
    base_revenue
    * (1 + premium_adoption / 100)
    * (1 + membership_growth / 200)
)

simulated_margin = (
    base_margin
    * (1 + aov_growth / 150)
    * (1 + premium_adoption / 200)
)

profit_impact = (
    simulated_revenue * (simulated_margin / 100)
)

# =========================================
# KPI CARDS
# =========================================

st.subheader("Executive Simulation Output")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Simulated Revenue",
    f"₹{round(simulated_revenue):,}"
)

col2.metric(
    "Projected AOV",
    f"₹{round(simulated_aov,2)}"
)

col3.metric(
    "Discount Dependency",
    f"{round(simulated_discount,2)}%"
)

col4.metric(
    "Projected Margin",
    f"{round(simulated_margin,2)}%"
)

# =========================================
# PROFIT IMPACT
# =========================================

st.subheader("Projected Profitability")

st.metric(
    "Estimated Profit Impact",
    f"₹{round(profit_impact):,}"
)

# =========================================
# COMPARISON TABLE
# =========================================

comparison_df = pd.DataFrame({
    "Metric": [
        "Revenue",
        "AOV",
        "Discount %",
        "Gross Margin"
    ],
    "Current": [
        round(base_revenue, 2),
        round(base_aov, 2),
        round(base_discount, 2),
        round(base_margin, 2)
    ],
    "Simulated": [
        round(simulated_revenue, 2),
        round(simulated_aov, 2),
        round(simulated_discount, 2),
        round(simulated_margin, 2)
    ]
})

st.subheader("Current vs Simulated")

st.dataframe(comparison_df)

# =========================================
# VISUAL COMPARISON
# =========================================

fig = px.bar(
    comparison_df,
    x="Metric",
    y=["Current", "Simulated"],
    barmode="group",
    title="Business Impact Comparison"
)

st.plotly_chart(fig, use_container_width=True)

# =========================================
# STRATEGIC INSIGHTS
# =========================================

st.subheader("Strategic Recommendations")

if simulated_discount < base_discount:
    st.success(
        "Reduced discount dependency improves long-term premium positioning."
    )

if simulated_aov > base_aov:
    st.success(
        "Higher AOV supports healthier unit economics and faster CAC recovery."
    )

if premium_adoption > 25:
    st.info(
        "Premium set adoption significantly boosts profitability and gifting behavior."
    )

if membership_growth > 20:
    st.info(
        "Membership expansion strengthens retention and long-term LTV growth."
    )

# =========================================
# FOOTER
# =========================================

st.markdown("---")

st.caption("""
Simulation system designed around the strategic objectives
identified in the Kross Kartel National Marketing Case Competition.
""")