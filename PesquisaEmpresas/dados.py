import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Top2000CompaniesGlobally.csv', delimiter=',')


#1. Quais países concentram o maior número de empresas entre as 2000 maiores do mundo?
#→ Insight: países com maior poder econômico global.
paises = df['Country']
counts = paises.value_counts()
#print(counts.head(5))

plt.bar(counts.index[:5], counts.values[:5], color='green')
plt.xlabel('País')
plt.ylabel('Número de empresas')
plt.show()

#2. Qual setor econômico domina a lista das maiores empresas?
#→ Insight: entender quais indústrias têm mais peso no PIB mundial.

#3. Existe correlação entre receita e lucro das empresas?
#→ Insight: mostra eficiência operacional entre setores.
