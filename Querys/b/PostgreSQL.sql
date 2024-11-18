SELECT * FROM orders WHERE order_id = 44;

UPDATE orders
SET status = 'Shipped'
WHERE order_id = 44;

SELECT * FROM orders WHERE order_id = 44;
