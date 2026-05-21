import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Bla Bli Blu Intelligence Platform",
    page_icon="📈",
    layout="wide"
)

# =========================================
# LOAD DATA
# =========================================

customers_df = pd.read_csv("data/synthetic/customers.csv")
orders_df = pd.read_csv("data/synthetic/orders.csv")
reviews_df = pd.read_csv("data/synthetic/reviews.csv")

# =========================================
# KPI CALCULATIONS
# =========================================

total_revenue = round(orders_df["order_value"].sum(), 2)

average_order_value = round(
    orders_df["order_value"].mean(),
    2
)

average_ltv = round(
    customers_df["lifetime_value"].mean(),
    2
)

repeat_purchase_rate = round(
    (
        len(customers_df[customers_df["total_orders"] > 1])
        / len(customers_df)
    ) * 100,
    2
)

avg_sentiment = round(
    reviews_df["sentiment_score"].mean(),
    2
)

# =========================================
# HEADER
# =========================================

st.title("📈 Bla Bli Blu Growth Intelligence Platform")

st.markdown("""
Executive intelligence system for modeling retention-led
growth strategies for premium D2C fragrance brands.
""")

# =========================================
# KPI ROW
# =========================================

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Revenue",
    f"₹{total_revenue:,.0f}"
)

col2.metric(
    "Average Order Value",
    f"₹{average_order_value}"
)

col3.metric(
    "Average LTV",
    f"₹{average_ltv}"
)

col4.metric(
    "Repeat Purchase Rate",
    f"{repeat_purchase_rate}%"
)

col5.metric(
    "Avg Sentiment Score",
    avg_sentiment
)

# =========================================
# REVENUE BY SEGMENT
# =========================================

st.subheader("Revenue Contribution by Customer Segment")

segment_revenue = (
    orders_df.groupby("customer_segment")["order_value"]
    .sum()
    .reset_index()
)

fig_segment = px.bar(
    segment_revenue,
    x="customer_segment",
    y="order_value",
    color="customer_segment",
    title="Revenue by Customer Segment"
)

st.plotly_chart(fig_segment, use_container_width=True)

# =========================================
# CUSTOMER SEGMENT DISTRIBUTION
# =========================================

st.subheader("Customer Segment Distribution")

segment_counts = (
    customers_df["customer_segment"]
    .value_counts()
    .reset_index()
)

segment_counts.columns = [
    "customer_segment",
    "count"
]

fig_pie = px.pie(
    segment_counts,
    names="customer_segment",
    values="count",
    title="Customer Segments"
)

st.plotly_chart(fig_pie, use_container_width=True)

# =========================================
# CONVERSION FUNNEL
# =========================================

st.subheader("Customer Lifecycle Funnel")

funnel_data = (
    orders_df["conversion_stage"]
    .value_counts()
    .reset_index()
)

funnel_data.columns = [
    "stage",
    "count"
]

fig_funnel = go.Figure(go.Funnel(
    y=funnel_data["stage"],
    x=funnel_data["count"]
))

fig_funnel.update_layout(
    title="Trial → Upsell → Repeat Funnel"
)

st.plotly_chart(fig_funnel, use_container_width=True)

# =========================================
# SENTIMENT ANALYSIS
# =========================================

st.subheader("Customer Emotion Distribution")

emotion_counts = (
    reviews_df["emotion"]
    .value_counts()
    .reset_index()
)

emotion_counts.columns = [
    "emotion",
    "count"
]

fig_emotion = px.bar(
    emotion_counts,
    x="emotion",
    y="count",
    color="emotion",
    title="Emotion Analysis"
)

st.plotly_chart(fig_emotion, use_container_width=True)

# =========================================
# DISCOUNT ANALYSIS
# =========================================

st.subheader("Discount Dependency by Segment")

discount_analysis = (
    orders_df.groupby("customer_segment")["discount_percent"]
    .mean()
    .reset_index()
)

fig_discount = px.bar(
    discount_analysis,
    x="customer_segment",
    y="discount_percent",
    color="customer_segment",
    title="Average Discount Usage"
)

st.plotly_chart(fig_discount, use_container_width=True)

# =========================================
# FOOTER
# =========================================

st.markdown("---")

st.caption("""
Built as part of a retention-led D2C growth intelligence initiative
inspired by the Kross Kartel National Marketing Case Competition.
""")