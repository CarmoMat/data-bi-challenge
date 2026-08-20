import psycopg2 
import os
import csv

pasta_csv = os.path.dirname(os.path.abspath(__file__))
lista_arquivos = os.listdir(pasta_csv)

# Conexão com o banco de dados PostgreSQL
# Antes de rodar, defina a variável de ambiente DB_PASSWORD com a senha do banco.
# PowerShell: $env:DB_PASSWORD = "sua_senha"
conexao = psycopg2.connect(
    host="localhost",
    port="5432",
    database="lh_nautical",
    user="postgres",
    password= os.environ.get("DB_PASSWORD")
)

print("Conexão com o banco de dados estabelecida com sucesso!")

cursor = conexao.cursor()

with open(os.path.join(pasta_csv, "schema.sql"), "r", encoding="utf-8") as file:
    schema_sql = file.read()
    cursor.execute(schema_sql)
    conexao.commit()
    
# Ajuste de tipos de dados para colunas específicas
cursor.execute("ALTER TABLE return_items ALTER COLUMN quantity TYPE REAL;")
cursor.execute("ALTER TABLE variant_attribute_values ALTER COLUMN value TYPE TEXT;")
    

# Percorre cada CSV da pasta e insere todas as linhas de dados na tabela correspondente do banco.
for arquivo in lista_arquivos:
    nome_tabela = arquivo.replace(".csv", "")
    if arquivo.endswith(".csv"):
        with open(os.path.join(pasta_csv, arquivo), "r", encoding="utf-8") as file:
            leitor = csv.reader(file)
            cabecalho = next(leitor)
            for linha in leitor:
                linha_tratada = [valor if valor != '' else None for valor in linha]  # Substitui valores vazios por None
                cursor.execute(f"INSERT INTO {nome_tabela} ({', '.join(cabecalho)}) VALUES ({', '.join(['%s'] * len(linha))})", linha_tratada) 
               # print(f"inserindo na tabela {nome_tabela}: a linha {linha} na coluna {cabecalho}")
    
    # Confirmar as alterações no banco de dados
    print(f"Arquivo {arquivo} processado com sucesso.")


conexao.commit()
print("Dados inseridos com sucesso!")

# Fechar o cursor e a conexão com o banco de dados
cursor.close()
conexao.close()
print("Conexão com o banco de dados encerrada.")