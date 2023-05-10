get_customers_with_birthday_today = """
SELECT customer_id, customer_first_name
FROM customer
WHERE EXTRACT(MONTH FROM birth_date) = EXTRACT(MONTH FROM CURRENT_DATE)
  AND EXTRACT(DAY FROM birth_date) = EXTRACT(DAY FROM CURRENT_DATE);
"""

get_top_products_for_year = """
SELECT p.product_name, SUM(t.quantity) as total_quantity
FROM transaction t
JOIN product p ON t.product_id = p.product_id
WHERE EXTRACT(YEAR FROM t.transaction_date) = :year
GROUP BY p.product_name
ORDER BY total_quantity DESC
LIMIT 10;
"""

get_last_order_per_customer = """
SELECT c.customer_id, c.customer_email, MAX(t.transaction_date) as last_order_date
FROM customer c
JOIN transaction t ON c.id = t.customer_id
GROUP BY c.customer_id, c.customer_email
ORDER BY c.customer_id;
"""