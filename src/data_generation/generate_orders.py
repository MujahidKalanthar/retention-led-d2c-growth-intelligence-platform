import pandas as pd
import random
from faker import Faker
from datetime import timedelta
import os

fake = Faker()

# -----------------------------
# CREATE OUTPUT DIRECTORY
# -----------------------------

os.makedirs("data/synthetic", exist_ok=True)

# -----------------------------
# LOAD EXISTING DATA
# -----------------------------

customers_df = pd.read_csv("data/synthetic/customers.csv")
products_df = pd.read_csv("data/synthetic/products.csv")

# -----------------------------
# CONFIG
# -----------------------------

TARGET_ORDERS = 150000

# -----------------------------
# ORDER STORAGE
# -----------------------------

orders = []

order_id = 100000

# -----------------------------
# SEGMENT-BASED ORDER LOGIC
# -----------------------------

for _, customer in customers_df.iterrows():

    customer_id = customer["customer_id"]
    segment = customer["customer_segment"]
    acquisition_date = pd.to_datetime(customer["acquisition_date"])

    total_orders = customer["total_orders"]

    for order_num in range(total_orders):

        # -----------------------------
        # ORDER DATE
        # -----------------------------

        days_after = random.randint(0, 700)

        order_date = acquisition_date + timedelta(days=days_after)

        # -----------------------------
        # PRODUCT SELECTION LOGIC
        # -----------------------------

        if segment == "Trial-Only":

            eligible_products = products_df[
                products_df["product_type"] == "Trial Pack"
            ]

        elif segment == "Premium Loyalist":

            eligible_products = products_df[
                products_df["product_type"].isin([
                    "100ml Bottle",
                    "Gift Set",
                    "Limited Edition"
                ])
            ]

        elif segment == "Fragrance Collector":

            eligible_products = products_df[
                products_df["product_type"].isin([
                    "100ml Bottle",
                    "Gift Set"
                ])
            ]

        elif segment == "Gifter":

            eligible_products = products_df[
                products_df["product_type"].isin([
                    "Gift Set",
                    "100ml Bottle"
                ])
            ]

        else:

            eligible_products = products_df

        # -----------------------------
        # RANDOM PRODUCT
        # -----------------------------

        product = eligible_products.sample(1).iloc[0]

        product_id = product["product_id"]
        product_type = product["product_type"]

        base_price = product["price"]

        # -----------------------------
        # DISCOUNT LOGIC
        # -----------------------------

        if segment == "Discount Seeker":
            discount_percent = random.randint(15, 40)

        elif segment == "Premium Loyalist":
            discount_percent = random.randint(0, 10)

        else:
            discount_percent = random.randint(5, 20)

        discount_amount = round(
            (discount_percent / 100) * base_price,
            2
        )

        final_order_value = round(
            base_price - discount_amount,
            2
        )

        # -----------------------------
        # SHIPPING + MARGIN
        # -----------------------------

        shipping_cost = random.randint(40, 180)

        gross_margin = round(
            final_order_value - product["cost"] - shipping_cost,
            2
        )

        # -----------------------------
        # GIFTING LOGIC
        # -----------------------------

        gifting_order = False

        if segment == "Gifter":
            gifting_order = random.choice([True, False])

        # -----------------------------
        # CONVERSION STAGE
        # -----------------------------

        if order_num == 0:
            conversion_stage = "Trial"

        elif order_num <= 2:
            conversion_stage = "Upsell"

        else:
            conversion_stage = "Repeat"

        # -----------------------------
        # SAVE ORDER
        # -----------------------------

        orders.append({
            "order_id": order_id,
            "customer_id": customer_id,
            "product_id": product_id,
            "order_date": order_date.date(),
            "product_type": product_type,
            "order_value": final_order_value,
            "discount_percent": discount_percent,
            "discount_amount": discount_amount,
            "shipping_cost": shipping_cost,
            "gross_margin": gross_margin,
            "gifting_order": gifting_order,
            "conversion_stage": conversion_stage,
            "customer_segment": segment,
            "acquisition_channel": customer["acquisition_channel"]
        })

        order_id += 1

# -----------------------------
# CREATE DATAFRAME
# -----------------------------

orders_df = pd.DataFrame(orders)

# -----------------------------
# SAVE CSV
# -----------------------------

output_path = "data/synthetic/orders.csv"

orders_df.to_csv(output_path, index=False)

# -----------------------------
# SUMMARY
# -----------------------------

print("Orders dataset generated successfully!")
print(f"Total orders created: {len(orders_df)}")
print(f"Saved to: {output_path}")

print("\nConversion Stage Distribution:")
print(orders_df["conversion_stage"].value_counts())

print("\nAverage Order Value:")
print(round(orders_df["order_value"].mean(), 2))