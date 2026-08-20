# Questão 4 - Análise de Clientes

## Contexto

A Diretoria da LH Nautical quer identificar clientes fiéis — quem tem gasto médio alto por transação E navega por diversas categorias da loja (não só quem compra muito uma única vez). O objetivo é mapear o que esses clientes de elite consomem, para replicar o comportamento em outros segmentos.

## Questão 4.1 - Código SQL

Ver `query.sql`

## O que essa consulta faz

Essa consulta encontra os 10 clientes que mais compram de forma variada e com valor alto por compra (os clientes "fiéis" que o desafio pede) e depois descobre qual categoria de produto esses 10 clientes mais compram.

Dividi em duas partes:

* **Parte A** — traz os 10 clientes com maior ticket médio, mas só os que compraram de 13 categorias diferentes ou mais.
* **Parte B** — pega esses mesmos 10 clientes e descobre qual categoria eles mais compraram (em quantidade de itens).

## Questão 4.2 - Explique

### Como você chegou nas categorias mais vendidas? (mapeamento da cadeia de chaves)

Pra saber a categoria de um produto comprado, precisei ir passando de tabela em tabela, porque não tem uma ligação direta entre pedido e categoria:

```text
orders → order_items → product_variants → products → categories
```

Cada `JOIN` une pela coluna que as duas tabelas compartilham (tipo `product_variant_id` ligando `order_items` com `product_variants`).

### Qual lógica utilizou para filtrar os clientes com diversidade mínima?

Usei `COUNT(DISTINCT categories.id)` pra contar quantas categorias diferentes cada cliente comprou, sem repetir.

Depois filtrei só quem tem 13 ou mais com:

```sql
WHERE diversidade >= 13
```

como pede o desafio.

### Como garantiu que a contagem de itens refletisse apenas os Top 10?

Na Parte B, criei uma CTE (`top10_clientes`) que repete o mesmo cálculo da Parte A e já filtra pra pegar só os 10 clientes certos.

Depois faço o `JOIN` dessa lista com `orders`, então só entram no cálculo os pedidos desses 10 clientes — nenhum outro cliente é contado.

---

## Detalhes adicionais

### Por que calculei faturamento separado, sem juntar com `order_items`

Se eu juntasse `orders` direto com `order_items` pra calcular o faturamento, um pedido com 3 itens apareceria 3 vezes, e eu ia somar o valor do pedido 3 vezes ao invés de 1.

Por isso calculei o faturamento e a frequência olhando só a tabela `orders`, sem juntar com os itens.