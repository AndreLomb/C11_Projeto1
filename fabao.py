import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Top2000CompaniesGlobally.csv', delimiter=',',encoding='utf-8')
plt.style.use('seaborn-v0_8')


#===================================================================================================================================
#1. Quais países concentram o maior número de empresas entre as 2000 maiores do mundo?

paises = df['Country']
counts1 = paises.value_counts()
top_countries = counts1[:10]
rest = counts1[10:].sum()

values = pd.concat([top_countries, pd.Series({'Outros': rest})])
plt.figure(figsize=(9, 9))
plt.pie(
    values,
    labels=values.index,
    autopct='%1.1f%%',
    startangle=90, #Angulo inicial onde o gráfico começa a desenhar a primeira fatia.
    pctdistance=0.85, #Distância entre o centro da pizza e o texto do percentual
    wedgeprops={'edgecolor': 'white'}, #adiciona uma linha branca entre as fatias
    colors=plt.cm.tab20.colors
)
plt.title('Distribuição das 2000 Maiores Empresas por País')
plt.show()
#===================================================================================================================================



#===================================================================================================================================
#2. Qual continente concentra o maior valor de mercado total?

valor_mercado_por_continente = df.groupby('Continent')['Market Value ($billion)'].sum().sort_values(ascending=False)

plt.bar(valor_mercado_por_continente.index, valor_mercado_por_continente.values, color='teal')
plt.xlabel('Continente')
plt.ylabel('Valor de Mercado Total (em bilhões de $)')
plt.title('Valor de Mercado Total por Continente')
plt.show()
#===================================================================================================================================



#===================================================================================================================================
#3. Existe correlação entre receita e lucro das empresas?

eficiencia = df['Profits ($billion)'] / df['Sales ($billion)']
eficiencia = eficiencia.replace([np.inf],0)

eficiencia_empresas = pd.DataFrame({'Company': df['Company'], 'Eficiencia': eficiencia})

max5 = eficiencia_empresas.nlargest(5, 'Eficiencia')
min5 = eficiencia_empresas.nsmallest(5, 'Eficiencia')

plt.bar(max5['Company'], max5['Eficiencia'], color='teal')
plt.xlabel('Empresa')
plt.ylabel('Eficiência (Lucro/Venda)')
plt.xticks(rotation=35, ha='right')   # gira e alinha os nomes
plt.tight_layout()                    # ajusta espaçamento automático
plt.title('Empresas mais eficientes (Lucro por venda)')
plt.tight_layout(rect=[0, 0, 1, 0.95]) #[esquerda, baixo, direita, cima] -> Termine o gráfico um pouco antes do topo (y=0.95 em vez de 1.0)
plt.show()
#===================================================================================================================================



#===================================================================================================================================
#4. Quais são as empresas com maior valor de mercado em cada continente?
#Africa, Asia, Europe, North America, Oceania, South America

mktvalue_continents = df.groupby('Continent')['Market Value ($billion)'].idxmax()
companies = df.loc[mktvalue_continents]
companies = companies.sort_values('Continent')

#Arrumando os valores para o gráfico
continents = companies['Continent']
company_names = companies['Company']
market_values = companies['Market Value ($billion)']

plt.close('all')
plt.style.use('seaborn-v0_8')
plt.figure(figsize=(14, 8))

# Criar barras com cores diferentes
bars = plt.bar(range(len(continents)), market_values, color='teal')

# Personalizar
plt.xticks(range(len(continents)), [f'{cont}\n({comp})' for cont, comp in zip(continents, company_names)],
           rotation=0, fontsize=10)

# Adicionar valores no topo das barras
for i, (bar, value) in enumerate(zip(bars, market_values)):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             f'${value}B', ha='center', va='bottom', fontweight='bold')

plt.ylabel('Valor de Mercado ($ Bilhões)', fontsize=12)
plt.title('Maiores Empresas por Valor de Mercado em Cada Continente', fontsize=14, fontweight='bold')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()
plt.close('all')
#===================================================================================================================================


#===================================================================================================================================
#5. Empresas com muitos ativos tendem a ser mais lucrativas?

plt.figure(figsize=(12, 8))
plt.scatter(df['Assets ($billion)'], df['Profits ($billion)'],
           alpha=0.6, color='teal', s=60)
plt.xlabel('Ativos ($bilhões)', fontsize=12)
plt.ylabel('Lucros ($bilhões)', fontsize=12)
plt.title('Relação entre Ativos Totais e Lucro', fontsize=14)
plt.grid(True, alpha=0.3)

# 1. Ajustar uma reta aos dados (regressão linear)
coeficiente_angular, coeficiente_linear = np.polyfit(
    df['Assets ($billion)'],  # Variável independente (X)
    df['Profits ($billion)'], # Variável dependente (Y)
    1                         # Grau do polinômio (1 = linha reta)
)

# 2. Criar função da linha de tendência
linha_tendencia = np.poly1d([coeficiente_angular, coeficiente_linear])

# 3. Plotar a linha de tendência
plt.plot(df['Assets ($billion)'],
         linha_tendencia(df['Assets ($billion)']),
         color='red',
         linestyle='--',
         alpha=0.8,
         label=f'Linha de Tendência (y = {coeficiente_angular:.2f}x + {coeficiente_linear:.2f})')

# Adicionar legenda
plt.legend()
plt.tight_layout()
plt.show()
#===================================================================================================================================



#===================================================================================================================================
#6. Quais as top10 empresas mais subvalorizadas?

df['Undervaluation'] = df['Assets ($billion)'] - df['Market Value ($billion)']
top10_sub = df.sort_values('Undervaluation', ascending=False).head(10)

# Scatter plot
plt.figure(figsize=(16,6))

# Todas as empresas em cinza
plt.scatter(df['Assets ($billion)'], df['Market Value ($billion)'], alpha=0.3, color='gray')

# Top 10 subvalorizadas em teal
plt.scatter(top10_sub['Assets ($billion)'], top10_sub['Market Value ($billion)'],
            alpha=0.8, color='teal', label='Top 10 Subvalorizadas')

# Adicionar nomes das top 10
for i, row in top10_sub.iterrows():
    plt.text(row['Assets ($billion)'] + 0.5, row['Market Value ($billion)'],
             row['Company'], fontsize=9, color='teal')

plt.xlabel('Ativos Totais (US$ bilhões)')
plt.ylabel('Valor de Mercado (US$ bilhões)')
plt.title('Relação entre Valor de Mercado e Ativos - Empresas Subvalorizadas')
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
#===================================================================================================================================

#===================================================================================================================================
#7. Quais países tem as empresas com maior lucro médio em relação à receita (Margem de Lucro)?

plt.close('all')
plt.style.use('seaborn-v0_8')

df['MargemLucro'] = (df['Profits ($billion)'] / df['Sales ($billion)']) * 100
df['MargemLucro'] = df['MargemLucro'].replace([np.inf, -np.inf], np.nan)

margem_pais = df.groupby('Country')['MargemLucro'].mean().sort_values(ascending=False)
top10_margem = margem_pais.head(10)

plt.figure(figsize=(12, 6))
bars = plt.bar(top10_margem.index, top10_margem.values, color='teal')
plt.title('Top 10 Países com Maior Margem de Lucro Média', fontsize=14)
plt.ylabel('Margem de Lucro Média (%)')
plt.xticks(rotation=45, ha='right')

for bar, val in zip(bars, top10_margem.values):
    plt.text(bar.get_x() + bar.get_width()/2, val + 0.5, f'{val:.1f}%', ha='center', fontsize=9)

plt.tight_layout()
plt.show()
#===================================================================================================================================



#===================================================================================================================================
#8. Há correlação entre o ranking e o valor de mercado (ou receita)?

plt.close('all')
plt.style.use('seaborn-v0_8')

corr_market = df['Global Rank'].corr(df['Market Value ($billion)'])
corr_sales = df['Global Rank'].corr(df['Sales ($billion)'])

plt.figure(figsize=(10, 5))
plt.scatter(df['Global Rank'], df['Market Value ($billion)'], alpha=0.6, color='teal')
plt.xlabel('Ranking Global')
plt.ylabel('Valor de Mercado (US$ bilhões)')
plt.title('Correlação entre Ranking e Valor de Mercado')
plt.grid(alpha=0.3)
plt.gca().invert_xaxis()  # Rank 1 à esquerda
plt.tight_layout()
plt.show()
#===================================================================================================================================



#===================================================================================================================================
#9. Qual continente concentra o maior número de empresas do ranking?
plt.close('all')
plt.style.use('seaborn-v0_8')

contagem_continente = df['Continent'].value_counts()

plt.figure(figsize=(8, 6))
plt.bar(contagem_continente.index, contagem_continente.values, color='teal')
plt.title('Número de Empresas por Continente', fontsize=14)
plt.ylabel('Quantidade de Empresas')
plt.xlabel('Continente')
plt.tight_layout()
plt.show()
#===================================================================================================================================



#===================================================================================================================================
#10. Qual a relação de margem de lucro das empresas no Top 10 do ranking?

plt.close('all')
plt.style.use('seaborn-v0_8')

top10 = df.nsmallest(10, 'Global Rank')[['Company', 'Sales ($billion)', 'Profits ($billion)', 'MargemLucro']]
media_top10 = top10['MargemLucro'].mean()
media_global = df['MargemLucro'].mean()

plt.figure(figsize=(12, 6))
bars = plt.bar(top10['Company'], top10['MargemLucro'], color='teal')
plt.title('Margem de Lucro (%) - Top 10 Empresas do Ranking Global', fontsize=14)
plt.ylabel('Margem de Lucro (%)')
plt.xticks(rotation=45, ha='right')

for bar, val in zip(bars, top10['MargemLucro']):
    plt.text(bar.get_x() + bar.get_width()/2, val + 0.5, f'{val:.1f}%', ha='center', fontsize=9)

plt.tight_layout()
plt.show()
#===================================================================================