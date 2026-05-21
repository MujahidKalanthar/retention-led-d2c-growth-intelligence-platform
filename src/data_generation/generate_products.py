import pandas as pd
import random
import os

# Create output directory if not exists
os.makedirs("data/synthetic", exist_ok=True)

# -----------------------------
# PRODUCT CATEGORIES
# -----------------------------

fragrance_categories = [
    "Woody",
    "Fresh",
    "Citrus",
    "Floral",
    "Oriental",
    "Spicy",
    "Aquatic"
]

# -----------------------------
# FRAGRANCE NAMES
# -----------------------------

fragrance_names = [
    "Midnight Oud",
    "Urban Pulse",
    "Velvet Ember",
    "Royal Mist",
    "Citrus Rush",
    "Ocean Noir",
    "Saffron Nights",
    "Golden Smoke",
    "Forest Drift",
    "Amber Code",
    "Silver Aura",
    "Crimson Spice",
    "Moonlit Musk",
    "Frozen Sage",
    "Velvet Bloom"
]

# -----------------------------
# PRODUCT TYPES
# -----------------------------

product_types = [
    "Trial Pack",
    "100ml Bottle",
    "Gift Set",
    "Discovery Set",
    "Limited Edition"
]

# -----------------------------
# GENERATE PRODUCTS
# -----------------------------

products = []

product_id = 1000

for fragrance in fragrance_names:

    category = random.choice(fragrance_categories)

    # Trial Pack
    trial_price = random.randint(199, 349)
    trial_cost = random.randint(70, 120)

    products.append({
        "product_id": product_id,
        "fragrance_name": fragrance,
        "category": category,
        "product_type": "Trial Pack",
        "size_ml": 10,
        "price": trial_price,
        "cost": trial_cost,
        "gross_margin": round(((trial_price - trial_cost) / trial_price) * 100, 2),
        "premium_score": random.randint(40, 65)
    })

    product_id += 1

    # 100ml Bottle
    bottle_price = random.randint(1799, 2999)
    bottle_cost = random.randint(450, 900)

    products.append({
        "product_id": product_id,
        "fragrance_name": fragrance,
        "category": category,
        "product_type": "100ml Bottle",
        "size_ml": 100,
        "price": bottle_price,
        "cost": bottle_cost,
        "gross_margin": round(((bottle_price - bottle_cost) / bottle_price) * 100, 2),
        "premium_score": random.randint(70, 95)
    })

    product_id += 1

# -----------------------------
# GENERATE GIFT SETS
# -----------------------------

gift_sets = [
    "Date Night Collection",
    "Corporate Power Collection",
    "Wedding Vows Collection",
    "Festive Glow Collection",
    "Summer Escape Collection"
]

for gift in gift_sets:

    set_price = random.randint(3999, 6999)
    set_cost = random.randint(1200, 2500)

    products.append({
        "product_id": product_id,
        "fragrance_name": gift,
        "category": "Curated Set",
        "product_type": "Gift Set",
        "size_ml": 300,
        "price": set_price,
        "cost": set_cost,
        "gross_margin": round(((set_price - set_cost) / set_price) * 100, 2),
        "premium_score": random.randint(85, 100)
    })

    product_id += 1

# -----------------------------
# CREATE DATAFRAME
# -----------------------------

products_df = pd.DataFrame(products)

# -----------------------------
# SAVE CSV
# -----------------------------

output_path = "data/synthetic/products.csv"

products_df.to_csv(output_path, index=False)

print("Products dataset generated successfully!")
print(f"Total products created: {len(products_df)}")
print(f"Saved to: {output_path}")