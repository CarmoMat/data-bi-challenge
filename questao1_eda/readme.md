# Questão 1 - EDA

## Contexto

O Sr. Almir quer saber: "Posso confiar nesses dados para tomar decisões?" O objetivo é fazer uma análise exploratória inicial na tabela `orders` — sem fazer nenhuma limpeza ou tratamento, apenas observar, agregar e descrever.

## Código

Ver `query.sql`

## Questão 1.2 - Validação

**Qual é o valor médio registrado na coluna "total"?**

R$ 28.704,99

## Questão 1.3 - Interpretação

**Com base na análise exploratória realizada, escreva um breve diagnóstico sobre a confiabilidade da tabela orders para análises futuras. Comente sobre:**

### Possíveis outliers em "total"

Usei o método IQR para identificar os possíveis outliers em total e encontrei 452 pedidos acima do limite de R$82.598, cerca de 0,92% do total. Como é uma proporção baixa, acredito que esses valores possam representar pedidos de maior valor, e não erro nos dados.

### Qualidade dos dados (valores nulos ou inconsistentes)

Pelas verificações que fiz existem valores nulos na coluna "salesperson_id", sendo 24.131 registros (cerca de 49,25%), o que parece bastante à primeira vista. Porém, ao comparar com a coluna "channel", percebi que todos esses nulos estão nos pedidos do canal e-commerce. Então, nesse caso, não parece ser um problema nos dados, mas algo provavelmente esperado, já que esses pedidos não possuem um vendedor associado. Por último também verifiquei as outras colunas e não encontrei valores inconsistentes, como "total" zerado ou negativo e datas fora do período dos dados.

### Considera que a tabela orders está pronta para análises ou exigiria tratamento prévio ou relacionamento com demais tabelas?

Como dito na primeira pergunta, os dados da tabela orders parecem confiáveis. Os outliers são poucos, os valores nulos encontrados têm uma explicação e não encontrei outras inconsistências relevantes. Porém adiciono que a tabela orders é apenas uma parte dos dados, então para análises mais completas vai ser necessário relacioná-la com as outras tabelas.