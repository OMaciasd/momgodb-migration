SELECT o.order_id, oi.product_id, p.name AS product_name, w.name AS warehouse_name
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN inventories i ON oi.product_id = i.product_id
INNER JOIN warehouse w ON i.warehouse_id = w.warehouse_id
WHERE w.name = 'Central Warehouse';
