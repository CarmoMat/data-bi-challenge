---Parte 1 - Visão geral da tabela orders
--Quantidade total de linhas
SELECT COUNT(*) 
FROM orders;

--Quantidade total de colunas
SELECT COUNT(*)
FROM information_schema.columns 
WHERE table_schema = 'public' AND table_name = 'orders';

--Intervalo de datas analisado (data mínima e máxima) da coluna created_at
SELECT MIN(created_at),  MAX(created_at)
FROM orders;


---Parte 2 - Análise de valores numéricos
SELECT MIN(total), MAX(total), AVG(total) AS media
FROM orders;

