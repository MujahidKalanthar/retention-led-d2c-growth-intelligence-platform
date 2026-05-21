import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Market Intelligence",
    layout="wide"
)

# =========================================
# LOAD DATA
# =========================================

reviews_df = pd.read_csv("data/synthetic/reviews.csv")

# =========================================
# HEADER
# =========================================

st.title("🧠 Consumer & Market Intelligence")

st.markdown("""
AI-powered sentiment and behavioral intelligence layer
for analyzing fragrance market perception, customer emotion,
and premium brand signals.
""")

# =========================================
# KPI METRICS
# =========================================

avg_sentiment = round(
    reviews_df["sentiment_score"].mean(),
    2
)

avg_rating = round(
    reviews_df["rating"].mean(),
    2
)

gifting_mentions = reviews_df["mention_gifting"].sum()

price_mentions = reviews_df["mention_price"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Sentiment",
    avg_sentiment
)

col2.metric(
    "Average Rating",
    avg_rating
)

col3.metric(
    "Gifting Mentions",
    gifting_mentions
)

col4.metric(
    "Price Sensitivity Mentions",
    price_mentions
)

# =========================================
# EMOTION DISTRIBUTION
# =========================================

st.subheader("Consumer Emotion Distribution")

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
# REVIEW SOURCE ANALYSIS
# =========================================

st.subheader("Review Source Intelligence")

source_counts = (
    reviews_df["source"]
    .value_counts()
    .reset_index()
)

source_counts.columns = [
    "source",
    "count"
]

fig_source = px.pie(
    source_counts,
    names="source",
    values="count",
    title="Review Source Distribution"
)

st.plotly_chart(fig_source, use_container_width=True)

# =========================================
# PRODUCT SENTIMENT ANALYSIS
# =========================================

st.subheader("Top Product Sentiment")

product_sentiment = (
    reviews_df.groupby("product_name")
    .agg({
        "sentiment_score": "mean",
        "rating": "mean"
    })
    .reset_index()
)

fig_product = px.scatter(
    product_sentiment,
    x="rating",
    y="sentiment_score",
    size="rating",
    color="product_name",
    title="Product Perception Mapping"
)

st.plotly_chart(fig_product, use_container_width=True)

# =========================================
# FEATURE MENTION ANALYSIS
# =========================================

st.subheader("Feature Mention Analysis")

feature_df = pd.DataFrame({
    "Feature": [
        "Longevity",
        "Pricing",
        "Gifting"
    ],
    "Mentions": [
        reviews_df["mention_longevity"].sum(),
        reviews_df["mention_price"].sum(),
        reviews_df["mention_gifting"].sum()
    ]
})

fig_features = px.bar(
    feature_df,
    x="Feature",
    y="Mentions",
    color="Feature",
    title="Key Consumer Discussion Themes"
)

st.plotly_chart(fig_features, use_container_width=True)

# =========================================
# WORD CLOUD
# =========================================

st.subheader("Consumer Language Intelligence")

all_reviews = " ".join(reviews_df["review_text"])

wordcloud = WordCloud(
    width=1000,
    height=500,
    background_color="white"
).generate(all_reviews)

fig, ax = plt.subplots(figsize=(12, 6))

ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")

st.pyplot(fig)

# =========================================
# NEGATIVE REVIEW ANALYSIS
# =========================================

st.subheader("Negative Sentiment Signals")

negative_reviews = reviews_df[
    reviews_df["sentiment_score"] < 0
]

st.dataframe(
    negative_reviews[
        [
            "product_name",
            "rating",
            "review_text",
            "source"
        ]
    ].head(10)
)

# =========================================
# STRATEGIC INSIGHTS
# =========================================

st.subheader("Market Intelligence Insights")

if avg_sentiment > 0.3:
    st.success(
        "Overall consumer sentiment indicates strong premium brand perception."
    )

if gifting_mentions > 500:
    st.info(
        "Gifting behavior appears to be a strong organic acquisition lever."
    )

if price_mentions > 300:
    st.warning(
        "Price sensitivity discussions suggest discount dependency risks."
    )

st.success(
    "Positive emotional language supports the transition from offer-led acquisition to signature loyalty positioning."
)

# =========================================
# FOOTER
# =========================================

st.markdown("---")

st.caption("""
Market intelligence system designed to analyze emotional,
behavioral, and premiumization signals in D2C fragrance ecosystems.
""")