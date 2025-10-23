import numpy as np  # Importa a biblioteca NumPy para cálculos numéricos e manipulação de arrays
import pandas as pd  # Importa o Pandas para manipulação de dados em formato de tabelas (DataFrames)
import matplotlib.pyplot as plt  # Importa o Matplotlib para criação de gráficos



df = pd.read_csv('Top2000CompaniesGlobally.csv', delimiter=',',encoding='utf-8')  # Lê o arquivo CSV com as 2000 maiores empresas
plt.style.use('seaborn-v0_8')  # Define o estilo visual dos gráficos como "seaborn"



#===================================================================================================================================
#1. Quais países concentram o maior número de empresas entre as 2000 maiores do mundo?

paises = df['Country']  # Seleciona a coluna 'Country' com o país de cada empresa
counts1 = paises.value_counts()  # Conta quantas empresas há em cada país
top_countries = counts1[:10]  # Seleciona os 10 países com mais empresas
rest = counts1[10:].sum()  # Soma o restante dos países (fora do top 10)

values = pd.concat([top_countries, pd.Series({'Outros': rest})])  # Junta o top 10 com o total de “Outros” países
plt.figure(figsize=(9, 9))  # Define o tamanho do gráfico de pizza
plt.pie(  # Cria o gráfico de pizza com os países
    values,
    labels=values.index,  # Define os nomes (países) como rótulos
    autopct='%1.1f%%',  # Mostra porcentagem com 1 casa decimal
    startangle=90,  # Começa o gráfico a partir do ângulo 90°
    pctdistance=0.85,  # Ajusta a distância do texto (porcentagem)
    wedgeprops={'edgecolor': 'white'},  # Define bordas brancas nos setores
    colors=plt.cm.tab20.colors  # Usa uma paleta de 20 cores
)
plt.title('Distribuição das 2000 Maiores Empresas por País')  # Título do gráfico
plt.show()  # Exibe o gráfico
#===================================================================================================================================



#===================================================================================================================================
#2. Qual continente concentra o maior valor de mercado total?

valor_mercado_por_continente = df.groupby('Continent')['Market Value ($billion)'].sum().sort_values(ascending=False)
# Agrupa por continente e soma o valor de mercado total, em ordem decrescente

plt.bar(valor_mercado_por_continente.index, valor_mercado_por_continente.values, color='teal')  # Cria gráfico de barras
plt.xlabel('Continente')  # Nome do eixo X
plt.ylabel('Valor de Mercado Total (em bilhões de $)')  # Nome do eixo Y
plt.title('Valor de Mercado Total por Continente')  # Título do gráfico
plt.show()  # Mostra o gráfico
#===================================================================================================================================



#===================================================================================================================================
#3. Existe correlação entre receita e lucro das empresas?

eficiencia = df['Profits ($billion)'] / df['Sales ($billion)']  # Calcula eficiência = lucro dividido pela venda
eficiencia = eficiencia.replace([np.inf],0)  # Substitui valores infinitos por 0

eficiencia_empresas = pd.DataFrame({'Company': df['Company'], 'Eficiencia': eficiencia})  # Cria novo DataFrame com empresa e eficiência

max5 = eficiencia_empresas.nlargest(5, 'Eficiencia')  # Seleciona as 5 empresas mais eficientes
min5 = eficiencia_empresas.nsmallest(5, 'Eficiencia')  # Seleciona as 5 menos eficientes

plt.bar(max5['Company'], max5['Eficiencia'], color='teal')  # Gráfico de barras para as 5 mais eficientes
plt.xlabel('Empresa')  # Rótulo eixo X
plt.ylabel('Eficiência (Lucro/Venda)')  # Rótulo eixo Y
plt.xticks(rotation=35, ha='right')  # Inclina os nomes das empresas
plt.tight_layout()  # Ajusta o layout
plt.title('Empresas mais eficientes (Lucro por venda)')  # Título do gráfico
plt.tight_layout(rect=[0, 0, 1, 0.95])  # Margens do gráfico
plt.show()  # Exibe o gráfico
#===================================================================================================================================



#===================================================================================================================================
#4. Quais são as empresas com maior valor de mercado em cada continente?

mktvalue_continents = df.groupby('Continent')['Market Value ($billion)'].idxmax()  # Pega o índice da empresa com maior valor de mercado por continente
companies = df.loc[mktvalue_continents]  # Seleciona essas empresas no DataFrame
companies = companies.sort_values('Continent')  # Ordena por continente

continents = companies['Continent']  # Lista de continentes
company_names = companies['Company']  # Nomes das empresas
market_values = companies['Market Value ($billion)']  # Valores de mercado

plt.close('all')  # Fecha gráficos anteriores
plt.style.use('seaborn-v0_8')  # Define o estilo seaborn
plt.figure(figsize=(14, 8))  # Define tamanho do gráfico

bars = plt.bar(range(len(continents)), market_values, color='teal')  # Cria barras de cada continente

plt.xticks(range(len(continents)), [f'{cont}\n({comp})' for cont, comp in zip(continents, company_names)],
           rotation=0, fontsize=10)  # Coloca o nome da empresa abaixo do continente

for i, (bar, value) in enumerate(zip(bars, market_values)):  # Escreve o valor em cima de cada barra
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             f'${value}B', ha='center', va='bottom', fontweight='bold')

plt.ylabel('Valor de Mercado ($ Bilhões)', fontsize=12)  # Nome eixo Y
plt.title('Maiores Empresas por Valor de Mercado em Cada Continente', fontsize=14, fontweight='bold')  # Título
plt.grid(axis='y', alpha=0.3)  # Grade horizontal
plt.tight_layout()  # Ajuste visual
plt.show()  # Exibe gráfico
plt.close('all')  # Fecha tudo
#===================================================================================================================================



#===================================================================================================================================
#5. Empresas com muitos ativos tendem a ser mais lucrativas?

plt.figure(figsize=(12, 8))  # Tamanho do gráfico
plt.scatter(df['Assets ($billion)'], df['Profits ($billion)'],
           alpha=0.6, color='teal', s=60)  # Cria gráfico de dispersão (ativos x lucro)
plt.xlabel('Ativos ($bilhões)', fontsize=12)  # Nome eixo X
plt.ylabel('Lucros ($bilhões)', fontsize=12)  # Nome eixo Y
plt.title('Relação entre Ativos Totais e Lucro', fontsize=14)  # Título
plt.grid(True, alpha=0.3)  # Grade

coeficiente_angular, coeficiente_linear = np.polyfit(  # Faz regressão linear (reta de tendência)
    df['Assets ($billion)'],
    df['Profits ($billion)'],
    1
)

linha_tendencia = np.poly1d([coeficiente_angular, coeficiente_linear])  # Cria função da linha de tendência

plt.plot(df['Assets ($billion)'],
         linha_tendencia(df['Assets ($billion)']),
         color='red',
         linestyle='--',
         alpha=0.8,
         label=f'Linha de Tendência (y = {coeficiente_angular:.2f}x + {coeficiente_linear:.2f})')  # Desenha a linha no gráfico

plt.legend()  # Mostra legenda
plt.tight_layout()  # Ajusta layout
plt.show()  # Exibe gráfico
#===================================================================================================================================



#===================================================================================================================================
#6. Quais as top10 empresas mais subvalorizadas?

df['Undervaluation'] = df['Assets ($billion)'] - df['Market Value ($billion)']  # Cria nova coluna de subvalorização (Ativos - Valor de mercado)
top10_sub = df.sort_values('Undervaluation', ascending=False).head(10)  # Seleciona as 10 mais subvalorizadas

plt.figure(figsize=(16,6))  # Tamanho do gráfico

plt.scatter(df['Assets ($billion)'], df['Market Value ($billion)'], alpha=0.3, color='gray')  # Dispersão geral
plt.scatter(top10_sub['Assets ($billion)'], top10_sub['Market Value ($billion)'],
            alpha=0.8, color='teal', label='Top 10 Subvalorizadas')  # Destaca as 10 subvalorizadas

for i, row in top10_sub.iterrows():  # Adiciona o nome de cada empresa no gráfico
    plt.text(row['Assets ($billion)'] + 0.5, row['Market Value ($billion)'],
             row['Company'], fontsize=9, color='teal')

plt.xlabel('Ativos Totais (US$ bilhões)')  # Eixo X
plt.ylabel('Valor de Mercado (US$ bilhões)')  # Eixo Y
plt.title('Relação entre Valor de Mercado e Ativos - Empresas Subvalorizadas')  # Título
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
#===================================================================================================================================
