import pandas as pd 
import os

diretorio = os.path.dirname(os.path.abspath(__file__))

# Carregando os arquivos CSV
products = pd.read_csv(os.path.join(diretorio, "products.csv"))
product_variants = pd.read_csv(os.path.join(diretorio, "product_variants.csv"))
orders = pd.read_csv(os.path.join(diretorio, "orders.csv"))
order_items = pd.read_csv(os.path.join(diretorio, "order_items.csv"))

bussola = products[products['name'] == 'Bússola de Bordo 702']

# Mesclando os DataFrames para obter as informações necessárias
df = bussola.merge(product_variants, left_on='id', right_on='product_id')
df = df.rename(columns={'id_x': 'produto_id', 'id_y': 'variante_id'})

df = df.merge(order_items, left_on='variante_id', right_on='product_variant_id')
df = df.rename(columns={'id': 'item_pedido_id'})

df = df.merge(orders, left_on='order_id', right_on='id')
df = df.rename(columns={'id': 'pedido_id'})

# Convertendo a coluna 'created_at' para o tipo datetime e criando uma coluna de ano e mês
df['created_at'] = pd.to_datetime(df['created_at'])
df['ano_mes'] = df['created_at'].dt.to_period('M')


vendas_mensais = df.groupby('ano_mes')['quantity'].sum()

# Dividindo os dados em treino e teste
treino = vendas_mensais[vendas_mensais.index <= '2025-12']
teste = vendas_mensais[(vendas_mensais.index >= '2026-01') & (vendas_mensais.index <= '2026-03')]

# Calculando as previsões usando a média dos últimos 3 meses
previsoes = {}
for mes in teste.index:
    tres_meses_antes = vendas_mensais[vendas_mensais.index < mes].tail(3)
    previsoes[mes] = tres_meses_antes.mean()

previsoes = pd.Series(previsoes)
print(f"Previsão para os próximos 3 meses:\n{previsoes}")

# Calculando o erro médio absoluto (MAE)
mae = (previsoes - teste).abs().mean()
print(f"\nErro médio absoluto (MAE): {mae}")


