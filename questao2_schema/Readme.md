# Questão 2 - Schema

## Contexto

O ERP não permite conexão direta com o banco de dados — a única forma de obter os dados é através dos CSVs fornecidos. O objetivo é desenvolver um código que detecta as colunas de cada tabela a partir dos CSVs e cria um arquivo `.sql` com as instruções de criação de cada tabela, usando apenas Python 3 puro (bibliotecas padrão), para um banco PostgreSQL.

## Questão 2.1 - Código Python

Ver `questao-2.py`

## Seção 1 - Script `questao-2.py`

### O que o script faz

Lê todos os arquivos CSV presentes na mesma pasta do script, identifica o nome das colunas de cada tabela e, com base no primeiro valor não-vazio de cada coluna, infere o tipo de dado mais adequado (`INTEGER`, `REAL`, `TIMESTAMP` ou `TEXT`).

Ao final, gera um arquivo `schema.sql` com as instruções `CREATE TABLE` para todas as tabelas, prontas para uso em um banco PostgreSQL.

### Como executar

1. Coloque o script na mesma pasta onde estão os arquivos CSV.
2. Execute com Python 3:
   `python questao-2.py`
3. O arquivo `schema.sql` será gerado automaticamente na mesma pasta.

### Lógica de inferência de tipo

A função `infer_type` segue esta ordem de verificação para cada coluna:

1. **Nome da coluna** - se contém palavras-chave como `cep`, `cpf`, `phone`, `sku`, `code`, `key` ou `tax`, o tipo é definido como `TEXT` diretamente (evitando tratar identificadores como CEP ou CPF como números).
2. **Data** - tenta interpretar o valor no formato `YYYY-MM-DD HH:MM:SS`; se bater, o tipo é `TIMESTAMP`.
3. **Inteiro** - verifica se o valor é composto só por dígitos; se sim, `INTEGER`.
4. **Decimal** - tenta converter para `float` (tratando vírgula como separador decimal); se funcionar, `REAL`.
5. **Caso nenhum dos anteriores se aplique**, o tipo é `TEXT` por padrão.

Se uma coluna não tiver nenhum valor de exemplo disponível (todos vazios), o script avisa no terminal e define o tipo como `TEXT` por segurança.

### Limitações conhecidas

- O tipo de cada coluna é definido a partir de apenas um valor de exemplo (o primeiro não-vazio encontrado), não da coluna inteira. Isso significa que colunas com valores mistos (ex: um número inteiro na primeira linha, mas decimais em outras) podem ser classificadas de forma imprecisa.
- Essa limitação foi identificada na prática durante a Questão 3 (carregamento dos dados), quando algumas colunas exigiram ajuste manual de tipo via `ALTER TABLE` após o schema já ter sido criado (mais detalhes na Seção 2).

---

## Seção 2 - Arquivo `schema.sql` gerado

### Resumo

O script gerou `CREATE TABLE` para as 24 tabelas correspondentes aos CSVs fornecidos, com tipos de dado inferidos automaticamente (`INTEGER`, `REAL`, `TIMESTAMP`, `TEXT`).

### Ajustes necessários após o carregamento real dos dados

Durante a Questão 3, ao tentar carregar os dados de fato no banco, três colunas precisaram de correção de tipo porque o valor de exemplo usado na inferência não representava toda a coluna:

- **`customers` / `suppliers` — `tax_id`**
  - Tipo inferido: `INTEGER`
  - Tipo corrigido: `TEXT`
  - Motivo: não era coberto pelas palavras-chave; é um identificador, não uma quantidade.

- **`return_items` — `quantity`**
  - Tipo inferido: `INTEGER`
  - Tipo corrigido: `REAL`
  - Motivo: existiam valores decimais além de inteiros.

- **`variant_attribute_values` — `value`**
  - Tipo inferido: `REAL`
  - Tipo corrigido: `TEXT`
  - Motivo: a coluna armazena atributos de tipos variados (números e texto).

Essas correções foram aplicadas via `ALTER TABLE` diretamente no script de carregamento (`load_schema.py`), documentadas em comentário no próprio código, preservando o `schema.sql` original gerado pela Q2.