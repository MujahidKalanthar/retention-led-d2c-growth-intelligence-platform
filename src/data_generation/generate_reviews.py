import pandas as pd
import random
from textblob import TextBlob
import os

# -----------------------------
# CREATE OUTPUT DIRECTORY
# -----------------------------

os.makedirs("data/synthetic", exist_ok=True)

# -----------------------------
# LOAD PRODUCTS
# -----------------------------

products_df = pd.read_csv("data/synthetic/products.csv")

# -----------------------------
# REVIEW TEMPLATES
# -----------------------------

positive_reviews = [
    "Absolutely loved the fragrance. Feels premium and lasts long.",
    "The packaging was beautiful and perfect for gifting.",
    "This scent feels luxurious and unique.",
    "One of the best fragrances I have tried recently.",
    "Loved the trial pack and ended up buying the full-size bottle.",
    "Perfect everyday fragrance. Got many compliments.",
    "Amazing scent projection and longevity.",
    "The gifting experience was fantastic.",
    "Smells expensive and classy.",
    "The fragrance wardrobe idea is brilliant."
]

neutral_reviews = [
    "The fragrance was decent but not very long-lasting.",
    "Packaging was okay and delivery was smooth.",
    "Good for daily use but expected better projection.",
    "Trial pack was useful for testing scents.",
    "Some fragrances were stronger than others.",
    "The scent profile was average for the price."
]

negative_reviews = [
    "The fragrance faded too quickly.",
    "Expected better quality for the price.",
    "Packaging looked premium but scent did not last.",
    "Too expensive compared to competitors.",
    "Did not enjoy the fragrance profile.",
    "The bottle leaked during delivery.",
    "Would not repurchase this fragrance.",
    "Discounts are good but full prices feel high."
]

# -----------------------------
# REVIEW SOURCES
# -----------------------------

sources = [
    "Amazon",
    "Nykaa",
    "Reddit",
    "Instagram",
    "Google Reviews"
]

# -----------------------------
# GENERATE REVIEWS
# -----------------------------

reviews = []

review_id = 1

NUM_REVIEWS = 5000

for _ in range(NUM_REVIEWS):

    product = products_df.sample(1).iloc[0]

    sentiment_type = random.choices(
        ["positive", "neutral", "negative"],
        weights=[60, 25, 15],
        k=1
    )[0]

    # -----------------------------
    # SELECT REVIEW TEXT
    # -----------------------------

    if sentiment_type == "positive":
        review_text = random.choice(positive_reviews)
        rating = random.randint(4, 5)

    elif sentiment_type == "neutral":
        review_text = random.choice(neutral_reviews)
        rating = random.randint(3, 4)

    else:
        review_text = random.choice(negative_reviews)
        rating = random.randint(1, 2)

    # -----------------------------
    # NLP SENTIMENT SCORE
    # -----------------------------

    sentiment_score = round(
        TextBlob(review_text).sentiment.polarity,
        2
    )

    # -----------------------------
    # EMOTION TAGGING
    # -----------------------------

    if sentiment_score > 0.4:
        emotion = "Excitement"

    elif sentiment_score > 0:
        emotion = "Satisfaction"

    elif sentiment_score == 0:
        emotion = "Neutral"

    else:
        emotion = "Disappointment"

    # -----------------------------
    # FEATURE MENTIONS
    # -----------------------------

    mention_longevity = "long" in review_text.lower() or "last" in review_text.lower()

    mention_price = "price" in review_text.lower() or "expensive" in review_text.lower()

    mention_gifting = "gift" in review_text.lower()

    # -----------------------------
    # SAVE REVIEW
    # -----------------------------

    reviews.append({
        "review_id": review_id,
        "product_id": product["product_id"],
        "product_name": product["fragrance_name"],
        "source": random.choice(sources),
        "rating": rating,
        "review_text": review_text,
        "sentiment_score": sentiment_score,
        "emotion": emotion,
        "mention_longevity": mention_longevity,
        "mention_price": mention_price,
        "mention_gifting": mention_gifting
    })

    review_id += 1

# -----------------------------
# CREATE DATAFRAME
# -----------------------------

reviews_df = pd.DataFrame(reviews)

# -----------------------------
# SAVE CSV
# -----------------------------

output_path = "data/synthetic/reviews.csv"

reviews_df.to_csv(output_path, index=False)

# -----------------------------
# SUMMARY
# -----------------------------

print("Reviews dataset generated successfully!")
print(f"Total reviews created: {len(reviews_df)}")
print(f"Saved to: {output_path}")

print("\nEmotion Distribution:")
print(reviews_df["emotion"].value_counts())

print("\nAverage Sentiment Score:")
print(round(reviews_df["sentiment_score"].mean(), 2))