SELECT status, COUNT(*) AS total_orders
FROM orders
GROUP BY status;
