Global E-Commerce Orders & Returns Dataset — 5 Related Tables 2024–2026
=======================================================================

Source: Synthetic — generated for analytics practice
Period: 2024 – 2026
Region: Global
Dataset page: https://prime-levels.com/data-hub/global-ecommerce-orders-returns-2024-2026

Files:
  - customers.csv  (3,000 rows, 12 columns)
  - products.csv  (345 rows, 10 columns)
  - orders.csv  (14,000 rows, 20 columns)
  - order_items.csv  (29,671 rows, 11 columns)
  - returns.csv  (2,433 rows, 15 columns)

How the tables relate:

A star schema with two dimensions and three facts, in a header-and-line shape.

customers (1) ──< orders      (many)  via customer_id
customers (1) ──< returns     (many)  via customer_id
products  (1) ──< order_items (many)  via product_id
products  (1) ──< returns     (many)  via product_id
orders    (1) ──< order_items (many)  via order_id
orders    (1) ──< returns     (many)  via order_id
order_items (1) ──< returns   (many)  via order_item_id

Build measures on order_items for anything product-level and on orders for anything basket-level; summing line totals and order totals together double counts.

Constraints that hold across the whole file:
- orders.gross_amount_local = SUM(order_items.line_total_local + line_discount_local) for that order
- orders.discount_local = SUM(order_items.line_discount_local); orders.items_count = SUM(order_items.quantity)
- orders.order_total_local = gross_amount_local − discount_local + shipping_fee_local + tax_local
- orders.order_total_usd = order_total_local / fx_rate_to_usd, and the same conversion holds on every line
- order_items.line_total_local = quantity × unit_price_local − line_discount_local
- a return exists only where orders.order_status = 'Delivered'
- returns.quantity_returned ≤ the quantity of the line it points at, and the refund never exceeds that line's total
- no order predates its customer's signup_date
- customers.lifetime_orders and lifetime_spend_usd are rolled up from non-cancelled orders

Synthetic data for analytics practice — it represents no real people or organizations.

prime-levels.com
