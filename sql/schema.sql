-- =========================================
-- CUSTOMERS TABLE
-- =========================================

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    age_group TEXT,
    city_tier TEXT,
    acquisition_channel TEXT,
    acquisition_date DATE,
    first_order_type TEXT,
    membership_status TEXT,
    customer_segment TEXT,
    total_orders INTEGER,
    avg_order_value REAL,
    lifetime_value REAL,
    repeat_purchase_rate REAL,
    referral_count INTEGER,
    churn_risk_score REAL,
    favorite_category TEXT
);

-- =========================================
-- PRODUCTS TABLE
-- =========================================

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    fragrance_name TEXT,
    category TEXT,
    product_type TEXT,
    size_ml INTEGER,
    price REAL,
    cost REAL,
    gross_margin REAL,
    premium_score INTEGER
);

-- =========================================
-- ORDERS TABLE
-- =========================================

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    order_date DATE,
    product_type TEXT,
    order_value REAL,
    discount_percent REAL,
    discount_amount REAL,
    shipping_cost REAL,
    gross_margin REAL,
    gifting_order BOOLEAN,
    conversion_stage TEXT,
    customer_segment TEXT,
    acquisition_channel TEXT,

    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
);

-- =========================================
-- REVIEWS TABLE
-- =========================================

CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    product_name TEXT,
    source TEXT,
    rating INTEGER,
    review_text TEXT,
    sentiment_score REAL,
    emotion TEXT,
    mention_longevity BOOLEAN,
    mention_price BOOLEAN,
    mention_gifting BOOLEAN,

    FOREIGN KEY(product_id) REFERENCES products(product_id)
);