#===================================================================================================================================
#7. Quais países têm as empresas com maior lucro médio em relação à receita (Margem de Lucro)?

plt.close('all')  # Fecha todos os gráficos anteriores
plt.style.use('seaborn-v0_8')  # Define novamente o estilo dos gráficos

df['MargemLucro'] = (df['Profits ($billion)'] / df['Sales ($billion)']) * 100  # Cria coluna com a margem de lucro em porcentagem
df['MargemLucro'] = df['MargemLucro'].replace([np.inf, -np.inf], np.nan)  # Substitui valores infinitos por NaN (ausentes)

margem_pais = df.groupby('Country')['MargemLucro'].mean().sort_values(ascending=False)  # Calcula a média da margem de lucro por país e ordena do maior para o menor
top10_margem = margem_pais.head(10)  # Seleciona os 10 países com maior margem média

plt.figure(figsize=(12, 6))  # Define tamanho do gráfico
bars = plt.bar(top10_margem.index, top10_margem.values, color='teal')  # Cria gráfico de barras
plt.title('Top 10 Países com Maior Margem de Lucro Média', fontsize=14)  # Título do gráfico
plt.ylabel('Margem de Lucro Média (%)')  # Nome do eixo Y
plt.xticks(rotation=45, ha='right')  # Rotaciona os nomes dos países para não sobrepor

for bar, val in zip(bars, top10_margem.values):  # Adiciona os valores numéricos acima de cada barra
    plt.text(bar.get_x() + bar.get_width()/2, val + 0.5, f'{val:.1f}%', ha='center', fontsize=9)

plt.tight_layout()  # Ajusta margens
plt.show()  # Mostra o gráfico
#===================================================================================================================================



#===================================================================================================================================
#8. Há correlação entre o ranking e o valor de mercado (ou receita)?

plt.close('all')  # Fecha gráficos anteriores
plt.style.use('seaborn-v0_8')  # Define o estilo visual

corr_market = df['Global Rank'].corr(df['Market Value ($billion)'])  # Calcula correlação entre ranking e valor de mercado
corr_sales = df['Global Rank'].corr(df['Sales ($billion)'])  # Calcula correlação entre ranking e receita

plt.figure(figsize=(10, 5))  # Define tamanho do gráfico
plt.scatter(df['Global Rank'], df['Market Value ($billion)'], alpha=0.6, color='teal')  # Gráfico de dispersão (ranking x valor de mercado)
plt.xlabel('Ranking Global')  # Nome eixo X
plt.ylabel('Valor de Mercado (US$ bilhões)')  # Nome eixo Y
plt.title('Correlação entre Ranking e Valor de Mercado')  # Título do gráfico
plt.grid(alpha=0.3)  # Adiciona uma grade suave
plt.gca().invert_xaxis()  # Inverte o eixo X (pois ranking 1 é o melhor)
plt.tight_layout()  # Ajuste de margens
plt.show()  # Exibe gráfico
#===================================================================================================================================



#===================================================================================================================================
#9. Qual continente concentra o maior número de empresas do ranking?

plt.close('all')  # Fecha gráficos anteriores
plt.style.use('seaborn-v0_8')  # Define estilo seaborn

contagem_continente = df['Continent'].value_counts()  # Conta quantas empresas há em cada continente

plt.figure(figsize=(8, 6))  # Define tamanho do gráfico
plt.bar(contagem_continente.index, contagem_continente.values, color='teal')  # Cria gráfico de barras
plt.title('Número de Empresas por Continente', fontsize=14)  # Título do gráfico
plt.ylabel('Quantidade de Empresas')  # Nome eixo Y
plt.xlabel('Continente')  # Nome eixo X
plt.tight_layout()  # Ajuste de margens
plt.show()  # Exibe gráfico
#===================================================================================================================================



#===================================================================================================================================
#10. Qual a relação de margem de lucro das empresas no Top 10 do ranking?

plt.close('all')  # Fecha gráficos anteriores
plt.style.use('seaborn-v0_8')  # Aplica o estilo seaborn

top10 = df.nsmallest(10, 'Global Rank')[['Company', 'Sales ($billion)', 'Profits ($billion)', 'MargemLucro']]
# Seleciona as 10 empresas com menor ranking (ou seja, top 10 melhores) e pega suas colunas principais

media_top10 = top10['MargemLucro'].mean()  # Calcula média da margem de lucro do top 10
media_global = df['MargemLucro'].mean()  # Calcula média da margem de lucro global (de todas as empresas)

plt.figure(figsize=(12, 6))  # Define tamanho do gráfico
bars = plt.bar(top10['Company'], top10['MargemLucro'], color='teal')  # Cria gráfico de barras com as margens do top 10
plt.title('Margem de Lucro (%) - Top 10 Empresas do Ranking Global', fontsize=14)  # Título
plt.ylabel('Margem de Lucro (%)')  # Nome eixo Y
plt.xticks(rotation=45, ha='right')  # Rotaciona nomes das empresas para melhor leitura

for bar, val in zip(bars, top10['MargemLucro']):  # Adiciona valores numéricos acima das barras
    plt.text(bar.get_x() + bar.get_width()/2, val + 0.5, f'{val:.1f}%', ha='center', fontsize=9)

plt.tight_layout()  # Ajuste final
plt.show()  # Exibe o gráfico
#===================================================================================
