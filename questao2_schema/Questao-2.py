import os
import csv
import datetime

# Este script deve ser executado a partir da mesma pasta onde os arquivos CSV estão localizados.
# Ele gera automaticamente o arquivo schema.sql na mesma pasta.


pasta_csv = os.path.dirname(os.path.abspath(__file__))
lista_arquivos = os.listdir(pasta_csv)
schemas = {}

# for pra percorrer a lista de arquivos e verificar se o arquivo é um csv,
# caso seja, abrir o arquivo e ler as colunas, armazenando no dicionário schemas 
# com o nome da tabela como chave e as colunas como valor.

for arquivo in lista_arquivos:
    if arquivo.endswith(".csv"):
        with open(os.path.join(pasta_csv, arquivo), "r", encoding="utf-8") as file:
            leitor = csv.reader(file)
            colunas = next(leitor)
            primeira_linha_dados = next(leitor)
            dict_colunas = dict(zip(colunas, primeira_linha_dados))
            nome_tabela = arquivo.replace(".csv", "")
            schemas[nome_tabela] = dict_colunas
                  
# Função para inferir o tipo de dado de uma coluna com base em seus valores.
    
def infer_type(coluna,nome_coluna):

    palavras_chave = ["cep", "cpf", "phone", "sku", "code", "key", "tax"]

    if any(palavra in nome_coluna for palavra in palavras_chave):
        return 'TEXT'
    else:
        primeiro_valor = None
        
        for valor in coluna:
            if valor == '':
                continue  # Ignora valores vazios
            primeiro_valor = valor
            break
        if primeiro_valor is None:
            print(f"Aviso: coluna '{nome_coluna}' sem valor de exemplo, tipo definido como TEXT por padrão") # print para depuração, caso a coluna esteja vazia
            return 'TEXT'  
            
        try:
            datetime.datetime.strptime(primeiro_valor, "%Y-%m-%d %H:%M:%S")
            return "TIMESTAMP"
        except ValueError:
            if primeiro_valor.isdigit():
                return 'INTEGER'
            else:
                try:
                    float(primeiro_valor.replace(',', '.'))  # Tenta converter para float, substituindo vírgula por ponto
                    return 'REAL'
                except ValueError:
                    return 'TEXT'
    
    
# Gerar o arquivo schema.sql com as instruções CREATE TABLE para cada tabela no dicionário schemas.

with open(os.path.join(pasta_csv, "schema.sql"), "w", encoding="utf-8") as file:    
    
    for nome_tabela, dict_colunas in schemas.items():
        
        sql_create_table = f"CREATE TABLE {nome_tabela} (\n"

        for nome_coluna, valor_exemplo in dict_colunas.items():
            tipo = infer_type([valor_exemplo], nome_coluna)
            sql_create_table += f"    {nome_coluna} {tipo},\n"
            

        sql_create_table = sql_create_table.rstrip(",\n") + "\n);"
        file.write(sql_create_table + "\n\n")
        

print("\nArquivo schema.sql gerado com sucesso na pasta:", pasta_csv)