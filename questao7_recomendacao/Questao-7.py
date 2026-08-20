import pandas as pd 
import os
from sklearn.metrics.pairwise import cosine_similarity

diretorio = os.path.dirname(os.path.abspath(__file__))

# Carregando os arquivos CSV
products = pd.read_csv(os.path.join(diretorio, "products.csv"))
product_variants = pd.read_csv(os.path.join(diretorio, "product_variants.csv"))
orders = pd.read_csv(os.path.join(diretorio, "orders.csv"))
order_items = pd.read_csv(os.path.join(diretorio, "order_items.csv"))

# Montando a matriz de interação entre clientes e produtos
df = order_items.merge(orders, left_on='order_id', right_on='id')

matriz = df.pivot_table(index='customer_id', columns='product_variant_id', aggfunc='size', fill_value=0)
matriz = (matriz > 0).astype(int)



# Calculando a similaridade entre os produtos usando a similaridade do cosseno
similaridade = cosine_similarity(matriz.T)

# Identificando o produto de referência
id_motor = products[products['name'] == 'Motor de Popa 1949']
variantes_motor = product_variants[product_variants['product_id'] == 180]
#print(variantes_motor)

produtos_ordem = matriz.columns
posicao_motor = produtos_ordem.get_loc(364)
# print(posicao_motor)

# Criando o ranking dos produtos mais similares ao motor
similaridade_motor = similaridade[363]
ranking = pd.Series(similaridade_motor, index=matriz.columns).sort_values(ascending=False)


# Selecionando os 5 produtos mais similares e descartando o próprio motor
top5_ids = ranking.index[1:6]
top5 = product_variants[product_variants['id'].isin(top5_ids)].merge(products, left_on='product_id', right_on='id')
print("os 5 produtos mais similares ao motor:")
print(top5[['sku', 'name']])