-- =========================================
-- TOTAL REVENUE
-- =========================================

SELECT
    ROUND(SUM(order_value), 2) AS total_revenue
FROM orders;

-- =========================================
-- AVERAGE ORDER VALUE (AOV)
-- =========================================

SELECT
    ROUND(AVG(order_value), 2) AS average_order_value
FROM orders;

-- =========================================
-- TOTAL CUSTOMERS
-- =========================================

SELECT
    COUNT(DISTINCT customer_id) AS total_customers
FROM customers;

-- =========================================
-- CUSTOMER LIFETIME VALUE (AVG)
-- =========================================

SELECT
    ROUND(AVG(lifetime_value), 2) AS average_ltv
FROM customers;

-- =========================================
-- REPEAT PURCHASE RATE
-- =========================================

SELECT
    ROUND(
        COUNT(
            CASE
                WHEN total_orders > 1 THEN 1
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS repeat_purchase_rate
FROM customers;

-- =========================================
-- GROSS MARGIN
-- =========================================

SELECT
    ROUND(AVG(gross_margin), 2) AS avg_gross_margin
FROM orders;

-- =========================================
-- DISCOUNT DEPENDENCY
-- =========================================

SELECT
    customer_segment,
    ROUND(AVG(discount_percent), 2) AS avg_discount
FROM orders
GROUP BY customer_segment
ORDER BY avg_discount DESC;

-- =========================================
-- TOP ACQUISITION CHANNELS
-- =========================================

SELECT
    acquisition_channel,
    COUNT(*) AS customer_count
FROM customers
GROUP BY acquisition_channel
ORDER BY customer_count DESC;