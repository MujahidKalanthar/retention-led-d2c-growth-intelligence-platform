-- =========================================
-- SEGMENT PERFORMANCE
-- =========================================

SELECT
    customer_segment,
    COUNT(*) AS total_customers,
    ROUND(AVG(lifetime_value), 2) AS avg_ltv,
    ROUND(AVG(avg_order_value), 2) AS avg_aov,
    ROUND(AVG(repeat_purchase_rate), 2) AS avg_repeat_rate,
    ROUND(AVG(churn_risk_score), 2) AS avg_churn_risk
FROM customers
GROUP BY customer_segment
ORDER BY avg_ltv DESC;

-- =========================================
-- MEMBERSHIP IMPACT
-- =========================================

SELECT
    membership_status,
    ROUND(AVG(lifetime_value), 2) AS avg_ltv,
    ROUND(AVG(total_orders), 2) AS avg_orders,
    ROUND(AVG(repeat_purchase_rate), 2) AS avg_repeat_rate
FROM customers
GROUP BY membership_status;

-- =========================================
-- HIGH VALUE CUSTOMERS
-- =========================================

SELECT
    customer_id,
    customer_segment,
    lifetime_value,
    total_orders
FROM customers
ORDER BY lifetime_value DESC
LIMIT 20;