SELECT p.product_id, p.name, p.price, c.name AS category_name
FROM products p
INNER JOIN product_categories c ON p.category_id = c.category_id
WHERE c.name = 'Electronics';
