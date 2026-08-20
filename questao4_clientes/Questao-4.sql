-- Questão 4.1
-- Parte A: Top 10 clientes por ticket médio (diversidade >= 13 categorias)

WITH faturamento_cliente AS (
    SELECT customer_id, SUM(total) AS faturamento_total, COUNT(*) AS frequencia
    FROM orders
    GROUP BY customer_id
), diversidade_cliente AS (
    SELECT orders.customer_id, COUNT(DISTINCT categories.id) AS diversidade
    FROM orders
    JOIN order_items 
    	ON orders.id = order_items.order_id
    JOIN product_variants 
    	ON order_items.product_variant_id = product_variants.id
    JOIN products 
    	ON product_variants.product_id = products.id
    JOIN categories 
    	ON products.category_id = categories.id
    GROUP BY orders.customer_id
)
SELECT faturamento_cliente.customer_id, faturamento_cliente.faturamento_total,
       faturamento_cliente.frequencia, diversidade_cliente.diversidade,
       faturamento_cliente.faturamento_total / faturamento_cliente.frequencia AS ticket_medio
FROM faturamento_cliente
JOIN diversidade_cliente 
	ON faturamento_cliente.customer_id = diversidade_cliente.customer_id
WHERE diversidade_cliente.diversidade >= 13
ORDER BY ticket_medio DESC, faturamento_cliente.customer_id ASC
LIMIT 10;


-- Parte B: Categoria mais comprada (em quantidade) entre esses 10 clientes

WITH faturamento_cliente AS (
    SELECT customer_id, SUM(total) AS faturamento_total, COUNT(*) AS frequencia
    FROM orders
    GROUP BY customer_id
), diversidade_cliente AS (
    SELECT orders.customer_id, COUNT(DISTINCT categories.id) AS diversidade
    FROM orders
    JOIN order_items 
    	ON orders.id = order_items.order_id
    JOIN product_variants 
    	ON order_items.product_variant_id = product_variants.id
    JOIN products 
    	ON product_variants.product_id = products.id
    JOIN categories 
    	ON products.category_id = categories.id
    GROUP BY orders.customer_id
), top10_clientes AS (
    SELECT faturamento_cliente.customer_id
    FROM faturamento_cliente
    JOIN diversidade_cliente 
    	ON faturamento_cliente.customer_id = diversidade_cliente.customer_id
    WHERE diversidade_cliente.diversidade >= 13
    ORDER BY faturamento_cliente.faturamento_total / faturamento_cliente.frequencia DESC,
             faturamento_cliente.customer_id ASC
    LIMIT 10
)

SELECT categories.name, SUM(order_items.quantity) AS total_itens
FROM top10_clientes
JOIN orders 
	ON orders.customer_id = top10_clientes.customer_id
JOIN order_items 
	ON orders.id = order_items.order_id
JOIN product_variants 
	ON order_items.product_variant_id = product_variants.id
JOIN products 
	ON product_variants.product_id = products.id
JOIN categories 
	ON products.category_id = categories.id
GROUP BY categories.name
ORDER BY total_itens DESC
LIMIT 1;