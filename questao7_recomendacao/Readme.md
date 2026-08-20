# Questão 7 - Sistema de Recomendação

## Contexto

A Marina quer implementar uma vitrine de "Quem comprou isso, também levou..." no site. O objetivo é criar um motor de recomendação baseado na similaridade de compra dos clientes, identificando qual produto deve ser recomendado junto ao "Motor de Popa 1949", sem usar ferramentas de Big Data — só similaridade de cosseno entre produtos.

## Questão 7.1 - Código Python

Ver `recomendacao.py`

## Questão 7.2 - Validação

**Qual é o nome do produto com MAIOR similaridade ao "Motor de Popa 1949"?**

Cabo Náutico 9307

## O que essa análise faz

O objetivo era criar um recomendador simples: dado o produto "Motor de Popa 1949", encontrar os 5 produtos mais similares com base nos clientes que compraram esses produtos.

A ideia é descobrir quais produtos costumam aparecer nas compras dos mesmos clientes.

## Questão 7.3 - Explique

### Como a matriz foi construída?

Uni `order_items` com `orders` pra descobrir qual cliente comprou cada produto.

Depois usei `pivot_table` para transformar esses dados em uma matriz:

* Cada linha representa um cliente (`customer_id`).
* Cada coluna representa um produto (`product_variant_id`).
* O valor é `1` se o cliente comprou aquele produto pelo menos uma vez e `0` caso contrário.

A quantidade comprada não é considerada, apenas se houve ou não a compra.

### O que significa a similaridade de cosseno nesse contexto?

A similaridade de cosseno serve pra comparar o padrão de clientes que compraram cada produto.

Por exemplo, se dois produtos foram comprados por muitos dos mesmos clientes, eles terão uma similaridade maior.

Como eu queria comparar os produtos entre si, e não os clientes, usei a matriz transposta (`matriz.T`) antes de calcular a similaridade.

### Uma limitação desse método de recomendação

Uma limitação é que a matriz considera apenas se o cliente comprou ou não o produto.

Então, um cliente que comprou um produto uma vez tem o mesmo peso que outro cliente que comprou várias vezes.

Além disso, o método considera apenas o comportamento de compra dos clientes e não características dos produtos, como preço, marca ou categoria.

---

## Detalhes adicionais

### Observação sobre o Motor de Popa 1949

O produto "Motor de Popa 1949" possui 3 variantes diferentes cadastradas.

Como a matriz foi criada usando `product_variant_id`, cada variante aparece separadamente.

Pra escolher uma delas como referência, verifiquei a quantidade de vendas de cada variante. A variante de `id = 364` foi a que teve mais vendas, com 154 vendas, então usei ela para gerar o ranking.

### Resultado completo

Os 5 produtos mais similares ao Motor de Popa 1949 foram:

1. **Cabo Náutico 9307**
2. **Tinta Antifouling 5779**
3. **GPS Pltoter 3205**
4. **Âncora Bruce 1231**
5. **Bússola de Bordo 4473**