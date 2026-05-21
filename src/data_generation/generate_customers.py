import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()

# Create output directory
os.makedirs("data/synthetic", exist_ok=True)

# -----------------------------
# CONFIG
# -----------------------------

NUM_CUSTOMERS = 50000

# -----------------------------
# OPTIONS
# -----------------------------

age_groups = [
    "18-24",
    "25-34",
    "35-44"
]

city_tiers = [
    "Tier 1",
    "Tier 2",
    "Tier 3"
]

acquisition_channels = [
    "Meta Ads",
    "Google Ads",
    "Organic Search",
    "Influencer",
    "Referral"
]

customer_segments = [
    "Discount Seeker",
    "Premium Loyalist",
    "Fragrance Collector",
    "Gifter",
    "Trial-Only",
    "Churn Risk"
]

fragrance_categories = [
    "Woody",
    "Fresh",
    "Floral",
    "Spicy",
    "Citrus",
    "Aquatic"
]

# -----------------------------
# DATE RANGE
# -----------------------------

start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 5, 1)

# -----------------------------
# GENERATE CUSTOMERS
# -----------------------------

customers = []

for customer_id in range(1, NUM_CUSTOMERS + 1):

    acquisition_date = fake.date_between(
        start_date=start_date,
        end_date=end_date
    )

    segment = random.choices(
        customer_segments,
        weights=[25, 20, 15, 10, 20, 10],
        k=1
    )[0]

    # Segment-based behavior modeling
    if segment == "Premium Loyalist":
        total_orders = random.randint(5, 15)
        avg_order_value = random.randint(2500, 6000)
        repeat_rate = round(random.uniform(0.6, 0.95), 2)
        membership = "Yes"
        churn_risk = round(random.uniform(0.05, 0.25), 2)

    elif segment == "Discount Seeker":
        total_orders = random.randint(1, 5)
        avg_order_value = random.randint(500, 1800)
        repeat_rate = round(random.uniform(0.1, 0.4), 2)
        membership = "No"
        churn_risk = round(random.uniform(0.5, 0.9), 2)

    elif segment == "Fragrance Collector":
        total_orders = random.randint(4, 12)
        avg_order_value = random.randint(3000, 7000)
        repeat_rate = round(random.uniform(0.5, 0.85), 2)
        membership = "Yes"
        churn_risk = round(random.uniform(0.1, 0.3), 2)

    elif segment == "Gifter":
        total_orders = random.randint(2, 8)
        avg_order_value = random.randint(2000, 5000)
        repeat_rate = round(random.uniform(0.3, 0.7), 2)
        membership = random.choice(["Yes", "No"])
        churn_risk = round(random.uniform(0.2, 0.5), 2)

    elif segment == "Trial-Only":
        total_orders = 1
        avg_order_value = random.randint(199, 499)
        repeat_rate = 0.0
        membership = "No"
        churn_risk = round(random.uniform(0.8, 1.0), 2)

    else:  # Churn Risk
        total_orders = random.randint(1, 3)
        avg_order_value = random.randint(500, 2000)
        repeat_rate = round(random.uniform(0.05, 0.2), 2)
        membership = "No"
        churn_risk = round(random.uniform(0.75, 0.98), 2)

    lifetime_value = total_orders * avg_order_value

    customers.append({
        "customer_id": customer_id,
        "age_group": random.choice(age_groups),
        "city_tier": random.choice(city_tiers),
        "acquisition_channel": random.choice(acquisition_channels),
        "acquisition_date": acquisition_date,
        "first_order_type": random.choice([
            "Trial Pack",
            "100ml Bottle"
        ]),
        "membership_status": membership,
        "customer_segment": segment,
        "total_orders": total_orders,
        "avg_order_value": avg_order_value,
        "lifetime_value": lifetime_value,
        "repeat_purchase_rate": repeat_rate,
        "referral_count": random.randint(0, 10),
        "churn_risk_score": churn_risk,
        "favorite_category": random.choice(fragrance_categories)
    })

# -----------------------------
# CREATE DATAFRAME
# -----------------------------

customers_df = pd.DataFrame(customers)

# -----------------------------
# SAVE CSV
# -----------------------------

output_path = "data/synthetic/customers.csv"

customers_df.to_csv(output_path, index=False)

print("Customers dataset generated successfully!")
print(f"Total customers created: {len(customers_df)}")
print(f"Saved to: {output_path}")

# -----------------------------
# BASIC SUMMARY
# -----------------------------

print("\nCustomer Segment Distribution:")
print(customers_df["customer_segment"].value_counts())