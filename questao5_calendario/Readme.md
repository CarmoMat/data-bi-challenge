# Questão 5 - Dimensão de Calendário

## Contexto

O Sr. Almir quer saber qual dia da semana tem a pior média de vendas nas lojas físicas, pra decidir se vale a pena fechar a loja nesses dias. Um estagiário calculou a média direto na tabela de vendas e concluiu que Domingo era ótimo — mas esqueceu que dias sem venda simplesmente não aparecem na tabela `orders`, inflando o resultado. O objetivo é corrigir isso construindo uma dimensão de calendário.

## Questão 5.1 - Código SQL

Ver `query.sql`

## O que essa consulta faz

O problema é que dias sem nenhuma venda não aparecem na tabela `orders`. Então, se eu simplesmente agrupasse por dia da semana direto na tabela de vendas, esses dias sem venda seriam ignorados e a média ficaria inflada.

Pra resolver isso, criei um calendário com todos os dias do período (mesmo os que não tiveram venda) e juntei com as vendas, preenchendo com zero os dias sem registro.

## Questão 5.2 - Explique

### Por que é necessário utilizar uma tabela de datas (calendário) em vez de agrupar diretamente a tabela de vendas?

Se eu agrupasse direto na tabela `orders`, só apareceriam os dias que têm venda registrada. Dias sem nenhuma venda simplesmente não existem na tabela, então eles desaparecem do cálculo — como se aquele dia nunca tivesse acontecido. Com o calendário, garanto que todos os dias do período aparecem, mesmo os sem venda, porque o calendário é gerado independente da tabela de vendas.

### O que aconteceria com a média de vendas se um dia da semana tivesse muitos dias sem nenhuma venda registrada?

A média ficaria artificialmente mais alta do que deveria. Isso porque, sem o calendário, esses dias sem venda simplesmente não entrariam na conta — a média seria calculada só em cima dos dias que tiveram venda, ignorando os zeros. Foi exatamente esse o erro do estagiário: Domingo parecia ótimo (R$5.000 de média) porque os domingos sem venda foram ignorados, quando na verdade deveriam contar como zero e puxar a média pra baixo.

---

## Detalhes adicionais

### Como montei o calendário

Usei `generate_series` pra gerar uma linha pra cada dia entre a menor data de venda em `orders` e a data de hoje (`CURRENT_DATE`).

Depois usei:

```sql
TO_CHAR(data, 'TMDay')
```

pra pegar o nome do dia da semana já em português.

### Como juntei o calendário com as vendas

Primeiro calculei as vendas por dia, considerando apenas lojas físicas:

```sql
WHERE channel = 'pos'
```

e agrupando por:

```sql
created_at::date
```

Isso faz com que a hora seja ignorada e apenas a data seja considerada.

Depois fiz um `LEFT JOIN` do calendário com essas vendas.

Usei `LEFT JOIN` (e não um `JOIN` normal) porque quero manter **todos** os dias do calendário na resposta, mesmo os que não têm nenhuma venda correspondente.

Nesses casos, os valores de venda vêm como `NULL`. Por isso, usei:

```sql
COALESCE(vendas_dia, 0)
```

para transformar esses `NULL` em zero.