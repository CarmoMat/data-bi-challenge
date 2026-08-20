# Questão 3 - Carregamento

## Contexto

Após a criação do schema, é necessário carregar os dados no banco para facilitar as análises posteriores. O carregamento deve cobrir todos os CSVs, respeitando o schema criado na Questão 2, sem fazer nenhum tratamento como remoção de nulos ou correção de caracteres especiais.

## Questão 3.1 - Código Python

Ver `load_schema.py`

## Questão 3.2 - Validação

**Qual o total de linhas somadas das seguintes tabelas: customers, orders, order_items e payments?**

251.864

## O que o script faz

Realiza o carregamento de todos os arquivos CSV presentes na mesma pasta do script para o banco de dados PostgreSQL `lh_nautical`.

O script utiliza o `schema.sql` gerado na Questão 2 para criar as tabelas e, em seguida, percorre todos os arquivos CSV, identificando automaticamente a tabela correspondente pelo nome do arquivo e inserindo todos os registros.

Para a conexão com o banco é utilizada a biblioteca `psycopg2`, enquanto a leitura dos arquivos CSV é realizada com a biblioteca nativa `csv` do Python.

### Como executar

1. Coloque o script `load_schema.py`, o `schema.sql` e todos os arquivos CSV na mesma pasta.
2. Defina a senha do PostgreSQL na variável de ambiente `DB_PASSWORD`.

No PowerShell:

```powershell
$env:DB_PASSWORD = "sua_senha"
```

3. Execute o script com Python 3:

```powershell
python load_schema.py
```

4. O script irá criar as tabelas a partir do `schema.sql` e carregar os dados dos arquivos CSV.

### Processo de carregamento

O script realiza as seguintes etapas:

1. Identifica automaticamente a pasta onde o script está localizado.
2. Lista os arquivos presentes na pasta.
3. Estabelece conexão com o banco PostgreSQL.
4. Executa o arquivo `schema.sql`.
5. Realiza os ajustes de tipo necessários em algumas colunas.
6. Percorre todos os arquivos com extensão `.csv`.
7. Utiliza o nome de cada arquivo como nome da tabela correspondente.
8. Lê o cabeçalho para identificar as colunas.
9. Percorre todas as linhas do arquivo.
10. Insere os registros na tabela correspondente.
11. Confirma as alterações com `commit`.
12. Fecha o cursor e a conexão com o banco.

### Valores vazios

Durante a leitura dos CSVs, valores vazios são convertidos para `None` antes da inserção:

```python
linha_tratada = [valor if valor != '' else None for valor in linha]
```

No PostgreSQL, esses valores são armazenados como `NULL`.

Esse procedimento não representa uma limpeza ou remoção de dados. Os valores vazios existentes nos arquivos são apenas convertidos para a representação correspondente no banco de dados.

### Ajustes de tipos

Durante o carregamento real dos dados, foram identificadas divergências entre alguns tipos definidos pelo `schema.sql` e os valores presentes em toda a coluna.

Para permitir o carregamento dos dados sem alterar seus valores, foram realizados os seguintes ajustes antes da inserção:

* **`return_items` / `quantity`**

  * Tipo original: `INTEGER`
  * Tipo ajustado: `REAL`
  * Motivo: a coluna possui valores decimais além de valores inteiros.

* **`variant_attribute_values` / `value`**

  * Tipo original: `REAL`
  * Tipo ajustado: `TEXT`
  * Motivo: a coluna pode armazenar valores de diferentes tipos, incluindo números e textos.

* **`customers` / `suppliers` — `tax_id`**

  * Tipo original: `INTEGER`
  * Tipo ajustado: `TEXT`
  * Motivo: a coluna funciona como identificador (CPF/CNPJ), não como quantidade numérica; não estava coberta pelas palavras-chave usadas na inferência de tipo da Questão 2.

Esses ajustes são realizados diretamente no script por meio de `ALTER TABLE`.

### Conexão com o banco

A conexão é realizada utilizando a biblioteca `psycopg2`:

```python
conexao = psycopg2.connect(
    host="localhost",
    port="5432",
    database="lh_nautical",
    user="postgres",
    password=os.environ.get("DB_PASSWORD")
)
```

A senha não é armazenada diretamente no código, sendo obtida por meio da variável de ambiente `DB_PASSWORD`.