-- =========================================
-- MONTHLY CUSTOMER COHORTS
-- =========================================

SELECT
    strftime('%Y-%m', acquisition_date) AS cohort_month,
    COUNT(customer_id) AS customers_acquired,
    ROUND(AVG(lifetime_value), 2) AS avg_ltv,
    ROUND(AVG(repeat_purchase_rate), 2) AS avg_repeat_rate
FROM customers
GROUP BY cohort_month
ORDER BY cohort_month;

-- =========================================
-- REPEAT CUSTOMERS BY COHORT
-- =========================================

SELECT
    strftime('%Y-%m', acquisition_date) AS cohort_month,
    COUNT(
        CASE
            WHEN total_orders > 1 THEN 1
        END
    ) AS repeat_customers
FROM customers
GROUP BY cohort_month
ORDER BY cohort_month;