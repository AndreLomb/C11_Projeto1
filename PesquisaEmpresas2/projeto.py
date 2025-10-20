import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('Top2000CompaniesGlobally.csv', delimiter=',', encoding='utf-8')

#Africa, Asia, Europe, North America, Oceania, South America
#4. Quais são as empresas com maior valor de mercado em cada continente?
mktvalue_continents = df.groupby('Continent')['Market Value ($billion)'].idxmax()
companies = df.loc[mktvalue_continents]
companies = companies.sort_values('Continent')
print("Empresas com maior valor de mercado /continente:\n",
      df.loc[:, ['Company','Continent','Market Value ($billion)']], '\n')

#Arrumando os valores para o gráfico
continents = companies['Continent']
company_names = companies['Company']
market_values = companies['Market Value ($billion)']

plt.close('all')
plt.figure(figsize=(14, 8))

# Criar barras com cores diferentes
colors = plt.cm.Set3(range(len(continents)))
bars = plt.bar(range(len(continents)), market_values, color=colors)

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

#=========================================================================================
#[Dedé]  5. Setores de tecnologia apresentam maior lucratividade média que os industriais?

#=========================================================================================

#[Dedé] 6. Quais as top10 empresas mais subvalorizadas? Existe relação entre o valor de mercado e o total de ativos de uma empresa?
profit_under = df.loc[:, ['Company', 'Market Value ($billion)', 'Assets ($billion)']]
profit_under = profit_under.sort_values('Market Value ($billion)', ascending=True)

print("Top 10 Empresas mais Subvalorizadas:\n", profit_under.head(10))

#Parte 1 - Gráfico das Empresas Subvalorizadas

# Selecionar top 10 empresas com menor valor de mercado
top10_sub = profit_under.head(10)

# Extrair dados
companies = top10_sub['Company']
market_values = top10_sub['Market Value ($billion)']

plt.figure(figsize=(12, 6))
bars = plt.barh(companies, market_values, color='salmon')

# Adicionar rótulos
for bar, value in zip(bars, market_values):
    plt.text(value + 1, bar.get_y() + bar.get_height()/2,
             f'${value:.1f}B', va='center', fontsize=9)

plt.xlabel('Valor de Mercado (US$ bilhões)')
plt.title('Top 10 Empresas Mais Subvalorizadas (Menor Market Cap)')
plt.gca().invert_yaxis()  # Inverter para mostrar da menor para a maior
plt.tight_layout()
plt.show()

#Parte 2 - Comparação entre valor de mercado e ativos
plt.figure(figsize=(10, 6))

plt.scatter(df['Assets ($billion)'],
            df['Market Value ($billion)'],
            alpha=0.6, color='teal')

plt.xlabel('Ativos Totais (US$ bilhões)')
plt.ylabel('Valor de Mercado (US$ bilhões)')
plt.title('Relação entre Valor de Mercado e Ativos')
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()