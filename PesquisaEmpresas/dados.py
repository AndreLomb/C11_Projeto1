import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Top2000CompaniesGlobally.csv', delimiter=',',encoding='utf-8')
plt.style.use('seaborn-v0_8')


#===================================================================================================================================
#1. Quais países concentram o maior número de empresas entre as 2000 maiores do mundo?
#→ Insight: países com maior poder econômico global.
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
#→ Insight: compara poder financeiro entre regiões do mundo.
valor_mercado_por_continente = df.groupby('Continent')['Market Value ($billion)'].sum().sort_values(ascending=False)

# Gráfico de barras
plt.bar(valor_mercado_por_continente.index, valor_mercado_por_continente.values, color='teal')
plt.xlabel('Continente')
plt.ylabel('Valor de Mercado Total (em bilhões de $)')
plt.title('Valor de Mercado Total por Continente')
plt.show()
#===================================================================================================================================



#===================================================================================================================================
#3. Existe correlação entre receita e lucro das empresas?
#→ Insight: mostra eficiência operacional entre setores.

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
#Insight: Há correlação entre ativos totais e lucro?

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

correlation = df['Assets ($billion)'].corr(df['Profits ($billion)'])
print(f"Coeficiente de correlação: {correlation:.3f}")

# Interpretação
if abs(correlation) > 0.7:
    strength = "forte"
elif abs(correlation) > 0.3:
    strength = "moderada"
else:
    strength = "fraca"

direction = "positiva" if correlation > 0 else "negativa"
print(f"Relação {strength} e {direction}s")

if correlation > 0.5:
    print("Empresas com mais ativos tendem a ser MAIS lucrativas")
elif correlation < -0.5:
    print("Empresas com mais ativos tendem a ser MENOS lucrativas")
else:
    print("Pouca evidência de relação entre ativos e lucratividade.\n")
#===================================================================================================================================



#===================================================================================================================================
#6. Quais as top10 empresas mais subvalorizadas? Existe relação entre o valor de mercado e o total de ativos de uma empresa?
profit_under = df.loc[:, ['Company', 'Market Value ($billion)', 'Assets ($billion)']]
profit_under = profit_under.sort_values('Market Value ($billion)', ascending=True)

print("Top 10 Empresas mais Subvalorizadas:\n", profit_under.head(10))

#Parte 1 - Gráfico das Empresas Subvalorizadas

# Selecionar top 10 empresas com menor valor de mercado
top10_sub = profit_under.head(10)

# Extrair dados
companies = top10_sub['Company']
market_values = top10_sub['Market Value ($billion)']

plt.figure(figsize=(16, 6))
bars = plt.barh(companies, market_values, color='teal')

# Adicionar rótulos
for bar, value in zip(bars, market_values):
    plt.text(value + 1, bar.get_y() + bar.get_height()/2,
             f'${value:.1f}B', va='center', fontsize=9)

plt.xlabel('Valor de Mercado (US$ bilhões)')
plt.title('Top 10 Empresas Mais Subvalorizadas (Menor Market Cap)')
plt.gca().invert_yaxis()  # Inverter para mostrar da menor para a maior
#plt.tight_layout()
plt.show()

#Parte 2 - Comparação entre valor de mercado e ativos
plt.figure(figsize=(16, 6))

plt.scatter(df['Assets ($billion)'],
            df['Market Value ($billion)'],
            alpha=0.6, color='teal')

plt.xlabel('Ativos Totais (US$ bilhões)')
plt.ylabel('Valor de Mercado (US$ bilhões)')
plt.title('Relação entre Valor de Mercado e Ativos')
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()
#===================================================================================================================================



