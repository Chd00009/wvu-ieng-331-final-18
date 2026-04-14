SELECT 
    seller_id,
    COUNT(*) AS total_orders
FROM order_items
WHERE seller_id = $1
GROUP BY seller_id;
