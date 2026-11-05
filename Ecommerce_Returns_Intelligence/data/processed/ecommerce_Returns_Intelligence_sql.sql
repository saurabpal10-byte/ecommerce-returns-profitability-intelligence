CREATE TABLE returns (
    return_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) REFERENCES orders(order_id),
    order_item_id VARCHAR(20) REFERENCES order_items(order_item_id),
    product_id VARCHAR(20) REFERENCES products(product_id),
    customer_id VARCHAR(20) REFERENCES customers(customer_id),
    return_date DATE,
    return_month VARCHAR(7),
    days_to_return INTEGER,
    quantity_returned INTEGER,
    return_reason VARCHAR(100),
    item_condition VARCHAR(30),
    refund_amount_local NUMERIC(14,2),
    refund_amount_usd NUMERIC(14,2),
    restocked VARCHAR(5),
    currency_code VARCHAR(5)
);

SELECT 'customers' AS table_name, COUNT(*) AS total_records FROM customers
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'returns', COUNT(*) FROM returns;

ALTER TABLE order_items
ADD CONSTRAINT fk_order_items_products
FOREIGN KEY (product_id)
REFERENCES products(product_id);

SELECT
    order_status,
    COUNT(*) AS total_orders,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;

SELECT
    order_status,
    COUNT(*) AS total_orders,
    ROUND(SUM(order_total_usd), 2) AS total_revenue_usd,
    ROUND(AVG(order_total_usd), 2) AS average_order_value_usd
FROM orders
GROUP BY order_status
ORDER BY total_revenue_usd DESC;


SELECT
    COUNT(*) AS total_order_items,
    ROUND(SUM(line_total_usd), 2) AS total_revenue_usd,
    ROUND(SUM(quantity * unit_cost_usd), 2) AS total_cost_usd,
    ROUND(SUM(line_profit_usd), 2) AS total_profit_usd,
    ROUND(
        SUM(line_profit_usd) * 100.0 /
        NULLIF(SUM(line_total_usd), 0),
        2
    ) AS profit_margin_percentage,
    COUNT(*) FILTER (WHERE line_profit_usd < 0)
        AS loss_making_items
FROM order_items;



SELECT
    p.product_id,
    p.product_name,
    p.category,
    COUNT(*) AS total_items_sold,
    COUNT(*) FILTER (
        WHERE oi.line_profit_usd < 0
    ) AS loss_making_items,
    ROUND(SUM(oi.line_profit_usd), 2) AS total_profit_usd,
    ROUND(
        SUM(oi.line_profit_usd) /
        NULLIF(COUNT(*), 0), 2
    ) AS avg_profit_per_item
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
HAVING COUNT(*) FILTER (
    WHERE oi.line_profit_usd < 0
) > 0
ORDER BY loss_making_items DESC
LIMIT 10;





SELECT
    return_reason,
    COUNT(*) AS total_returns,
    ROUND(SUM(refund_amount_usd), 2) AS total_refund_usd,
    ROUND(AVG(refund_amount_usd), 2) AS average_refund_usd
FROM returns
GROUP BY return_reason
ORDER BY total_returns DESC;





SELECT
    p.category,
    SUM(oi.quantity) AS total_units_sold,
    COALESCE(SUM(r.quantity_returned), 0) AS units_returned,
    ROUND(
        COALESCE(SUM(r.quantity_returned), 0) * 100.0 /
        NULLIF(SUM(oi.quantity), 0),
        2
    ) AS return_rate_percentage,
    ROUND(COALESCE(SUM(r.refund_amount_usd), 0), 2)
        AS total_refunds_usd
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
LEFT JOIN returns r
    ON oi.order_item_id = r.order_item_id
GROUP BY p.category
ORDER BY return_rate_percentage DESC;



WITH returns_by_item AS (
    SELECT
        order_item_id,
        SUM(quantity_returned) AS returned_qty,
        SUM(refund_amount_usd) AS refund_usd
    FROM returns
    GROUP BY order_item_id
)
SELECT
    p.category,
    SUM(oi.quantity) AS total_units_sold,
    SUM(COALESCE(r.returned_qty, 0)) AS units_returned,
    ROUND(
        SUM(COALESCE(r.returned_qty, 0)) * 100.0 /
        NULLIF(SUM(oi.quantity), 0),
        2
    ) AS return_rate_percentage,
    ROUND(SUM(COALESCE(r.refund_usd, 0)), 2)
        AS total_refunds_usd
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN returns_by_item r
    ON oi.order_item_id = r.order_item_id
GROUP BY p.category
ORDER BY return_rate_percentage DESC;


SELECT
    order_month,
    COUNT(*) AS delivered_orders,
    ROUND(SUM(order_total_usd), 2) AS monthly_revenue_usd,
    ROUND(AVG(order_total_usd), 2) AS average_order_value_usd
FROM orders
WHERE order_status = 'Delivered'
GROUP BY order_month
ORDER BY order_month;



CREATE OR REPLACE VIEW vw_monthly_revenue_trend AS
SELECT
    order_month,
    COUNT(*) AS delivered_orders,
    ROUND(SUM(order_total_usd), 2) AS monthly_revenue_usd,
    ROUND(AVG(order_total_usd), 2) AS average_order_value_usd
FROM orders
WHERE order_status = 'Delivered'
GROUP BY order_month
ORDER BY order_month;


SELECT *
FROM vw_monthly_revenue_trend
ORDER BY order_month
LIMIT 10;




CREATE OR REPLACE VIEW vw_category_return_analysis AS
WITH sales AS (
    SELECT
        p.category,
        SUM(oi.quantity) AS total_units_sold
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status = 'Delivered'
    GROUP BY p.category
),
returns AS (
    SELECT
        p.category,
        SUM(r.quantity_returned) AS units_returned,
        ROUND(SUM(r.refund_amount_usd), 2) AS total_refunds_usd
    FROM returns r
    JOIN order_items oi ON r.order_item_id = oi.order_item_id
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.category
)
SELECT
    s.category,
    s.total_units_sold,
    COALESCE(r.units_returned, 0) AS units_returned,
    ROUND(
        COALESCE(r.units_returned, 0) * 100.0
        / NULLIF(s.total_units_sold, 0), 2
    ) AS return_rate_percentage,
    COALESCE(r.total_refunds_usd, 0) AS total_refunds_usd
FROM sales s
LEFT JOIN returns r ON s.category = r.category
ORDER BY return_rate_percentage DESC;





SELECT *
FROM vw_category_return_analysis
ORDER BY return_rate_percentage DESC;



CREATE OR REPLACE VIEW vw_product_profitability AS
WITH product_sales AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        SUM(oi.quantity) AS units_sold,
        ROUND(SUM(oi.line_total_usd), 2) AS revenue_usd,
        ROUND(SUM(oi.quantity * oi.unit_cost_usd), 2) AS cost_usd,
        ROUND(SUM(oi.line_profit_usd), 2) AS profit_usd
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status = 'Delivered'
    GROUP BY p.product_id, p.product_name, p.category
),
product_returns AS (
    SELECT
        product_id,
        SUM(quantity_returned) AS units_returned
    FROM returns
    GROUP BY product_id
)
SELECT
    s.*,
    COALESCE(r.units_returned, 0) AS units_returned,
    ROUND(
        COALESCE(r.units_returned, 0) * 100.0
        / NULLIF(s.units_sold, 0), 2
    ) AS return_rate_percentage
FROM product_sales s
LEFT JOIN product_returns r ON s.product_id = r.product_id;



SELECT
    product_id,
    product_name,
    category,
    units_sold,
    revenue_usd,
    profit_usd,
    units_returned,
    return_rate_percentage
FROM vw_product_profitability
ORDER BY profit_usd DESC
LIMIT 10;


CREATE OR REPLACE VIEW vw_sales_channel_performance AS
SELECT
    sales_channel,
    COUNT(*) AS total_orders,
    ROUND(SUM(order_total_usd), 2) AS total_revenue_usd,
    ROUND(AVG(order_total_usd), 2) AS average_order_value_usd
FROM orders
WHERE order_status = 'Delivered'
GROUP BY sales_channel
ORDER BY total_revenue_usd DESC;


SELECT *
FROM vw_sales_channel_performance
ORDER BY total_revenue_usd DESC;



CREATE OR REPLACE VIEW vw_customer_value_analysis AS
WITH customer_metrics AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.country,
        c.region,
        c.acquisition_channel,
        COUNT(o.order_id) AS total_orders,
        ROUND(SUM(o.order_total_usd), 2) AS total_revenue_usd,
        ROUND(AVG(o.order_total_usd), 2) AS average_order_value_usd
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    WHERE o.order_status = 'Delivered'
    GROUP BY
        c.customer_id,
        c.customer_name,
        c.country,
        c.region,
        c.acquisition_channel
),
ranked_customers AS (
    SELECT *,
        NTILE(4) OVER (
            ORDER BY total_revenue_usd DESC
        ) AS revenue_quartile
    FROM customer_metrics
)
SELECT *,
    CASE revenue_quartile
        WHEN 1 THEN 'High Value'
        WHEN 2 THEN 'Mid-High Value'
        WHEN 3 THEN 'Mid-Low Value'
        WHEN 4 THEN 'Low Value'
    END AS customer_segment
FROM ranked_customers;


SELECT
    customer_segment,
    COUNT(*) AS total_customers,
    ROUND(SUM(total_revenue_usd), 2) AS segment_revenue_usd,
    ROUND(AVG(total_revenue_usd), 2) AS average_customer_revenue_usd
FROM vw_customer_value_analysis
GROUP BY customer_segment
ORDER BY average_customer_revenue_usd DESC;



CREATE OR REPLACE VIEW vw_monthly_return_trend AS
SELECT
    return_month,
    COUNT(*) AS total_returns,
    SUM(quantity_returned) AS units_returned,
    ROUND(SUM(refund_amount_usd), 2) AS total_refunds_usd,
    ROUND(AVG(refund_amount_usd), 2) AS average_refund_usd
FROM returns
GROUP BY return_month
ORDER BY return_month;


SELECT *
FROM vw_monthly_return_trend
ORDER BY return_month;



CREATE OR REPLACE VIEW vw_business_kpis AS
SELECT
    COUNT(*) FILTER (
        WHERE order_status = 'Delivered'
    ) AS delivered_orders,

    COUNT(*) FILTER (
        WHERE order_status = 'Cancelled'
    ) AS cancelled_orders,

    ROUND(
        SUM(order_total_usd) FILTER (
            WHERE order_status = 'Delivered'
        ), 2
    ) AS delivered_revenue_usd,

    ROUND(
        AVG(order_total_usd) FILTER (
            WHERE order_status = 'Delivered'
        ), 2
    ) AS average_order_value_usd,

    (
        SELECT ROUND(SUM(line_profit_usd), 2)
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.order_status = 'Delivered'
    ) AS delivered_profit_usd,

    (
        SELECT COUNT(*)
        FROM returns
    ) AS total_returns,

    (
        SELECT ROUND(SUM(refund_amount_usd), 2)
        FROM returns
    ) AS total_refunds_usd
FROM orders;


SELECT * FROM vw_business_kpis;



CREATE OR REPLACE VIEW vw_order_status_analysis AS
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status;



CREATE OR REPLACE VIEW vw_return_reason_analysis AS
SELECT
    return_reason,
    COUNT(*) AS total_returns,
    ROUND(SUM(refund_amount_usd), 2) AS total_refunds_usd
FROM returns
GROUP BY return_reason
ORDER BY total_returns DESC;


SELECT table_name
FROM information_schema.views
WHERE table_schema = 'public'
ORDER BY table_name;

SELECT * FROM vw_business_kpis;