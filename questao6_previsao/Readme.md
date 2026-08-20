# Questão 6 - Previsão de Demanda

## Contexto

O Sr. Almir quer um modelo preditivo confiável pra ajustar as compras com fornecedores, depois de ter perdido vendas por falta de estoque de um produto e comprado excesso de outro só no "feeling". O objetivo é prever a demanda mensal do produto "Bússola de Bordo 702" para o primeiro trimestre de 2026, usando um baseline de média móvel dos últimos 3 meses, sem usar dados futuros (data leakage).

## Questão 6.1 - Código Python

Ver `previsao_demanda.py`

## Questão 6.2 - Validação

**Utilizando seu modelo treinado, qual é a soma total da previsão de vendas (arredondada para número inteiro) para o 'Bússola de Bordo 702' durante o primeiro trimestre de 2026?**

149 unidades

## Questão 6.3 - Explique

### Como o baseline foi construído?

Separei os dados em:

* **Treino:** até dezembro de 2025.
* **Teste:** janeiro a março de 2026.

Para cada mês do teste, a previsão foi calculada como a média dos **3 meses imediatamente anteriores**, utilizando sempre os valores reais disponíveis.

Por exemplo, para prever fevereiro/2026, usei a média de novembro/2025, dezembro/2025 e janeiro/2026. Janeiro é utilizado como valor real, pois já teria acontecido quando a empresa fosse tomar a decisão de compra para fevereiro.

### Como evitou data leakage?

Em nenhum momento utilizei dados de um mês **posterior** ao mês que estava sendo previsto.

A regra utilizada foi: para cada previsão, só podem ser utilizados meses que já aconteceram em relação ao mês previsto, sejam eles do conjunto de treino ou do teste. Nunca foi utilizado um mês futuro para gerar uma previsão.

### Uma limitação do modelo proposto

Uma limitação é que a média móvel pode demorar para acompanhar mudanças na demanda. Como ela usa a média dos últimos 3 meses, os meses mais antigos continuam influenciando a previsão mesmo quando as vendas começam a aumentar ou diminuir.

## Respostas objetivas

### a. O baseline é adequado para esse produto?

Parcialmente. A média das vendas reais foi de 69 unidades e o MAE foi de 19,44, então o erro é considerável. Em janeiro o erro foi bem maior, mas em março ficou bem menor. Isso mostra que a média móvel funciona melhor quando as vendas estão mais estáveis, mas tem dificuldade quando acontece uma mudança maior na demanda.

### b. Cite uma limitação desse método

Uma limitação é que a média móvel pode demorar para acompanhar mudanças na demanda. Como ela usa a média dos últimos 3 meses, os meses mais antigos continuam influenciando a previsão mesmo quando as vendas começam a aumentar ou diminuir.

---

## Detalhes adicionais

### Observação importante sobre o produto

Ao filtrar `products` pelo nome "Bússola de Bordo 702", encontrei **dois produtos diferentes** cadastrados com esse mesmo nome (IDs 74 e 240), de marcas e categorias diferentes.

Como o enunciado pede pra considerar "o produto" no singular, mas os dados mostram dois cadastros distintos, optei por tratar os dois como uma demanda agregada — somando as vendas dos dois, como se fossem a mesma linha de produto vendida ao cliente final.

### Como montei o dataset

Uni as tabelas na seguinte ordem, cada uma trazendo a informação que faltava pra próxima etapa:

```text
products → product_variants → order_items → orders
```

* `products` → `product_variants`: pra pegar as variantes do produto filtrado.
* `product_variants` → `order_items`: pra pegar os itens realmente comprados.
* `order_items` → `orders`: pra pegar a data de cada pedido (`created_at`).

Depois de cada merge, renomeei as colunas `id` repetidas (que o pandas cria automaticamente como `id_x`/`id_y`), pra evitar conflito nos próximos merges.

### Como agreguei por mês

Converti `created_at` pra tipo data usando `pd.to_datetime`, depois usei `.dt.to_period('M')` pra extrair o ano e mês de cada pedido.

Por fim, agrupei os dados por mês usando `groupby` e somei a coluna `quantity` para obter a demanda mensal.

### Resultado (MAE)

O erro médio absoluto (MAE) da previsão foi de aproximadamente **19,44 unidades por mês** — a diferença absoluta média entre a quantidade prevista e a quantidade realmente vendida em cada mês do primeiro trimestre de 2026.