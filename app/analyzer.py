#import bibliotek
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

#wyswietlenie zawartości katalogu z opiniami
print(*os.listdir('./opinions_json'))

#wczytanie identyfiaktora produktu, którego opinie będą analizowane
product_id = input('Podaj kod produktu: ')

#wczytanie do ramki danych opinii z pliku
opinions = pd.read_json('./opinions_json/'+product_id+'.json')
opinions = opinions.set_index('opinion_id')

opinions['stars'] = opinions['stars'].map(lambda x: float(x.split('/')[0].replace(',','.')))

#częstość występowania poszczególnej liczby gwiazdek
stars = opinions['stars'].value_counts().sort_index().reindex(list(np.arange(0, 5.1, 0.5)), fill_value=0)
fig, ax = plt.subplots()
stars.plot.bar(color = 'darkorange')
plt.xticks(rotation=0)
ax.set_title('Ilość danych ocen')
ax.set_xlabel('Liczba gwiazdek')
ax.set_ylabel('Liczba opinii')
plt.savefig('./figures_png/'+product_id+'_bar.png')
plt.close()

#udział poszczególnych rekomendacji w ogólnej liczbie opinii
recommendation = opinions['recommendation'].value_counts()
fig, ax = plt.subplots()
recommendation.plot.pie(label = '', autopct= '%.1f%%', colors = ['darkorange', 'bisque'])
ax.set_title('Rekomendacje')
plt.savefig('./figures_png/'+product_id+'_pie.png')
plt.close()

#podstawowe statystki
stars_avarage = opinions['stars'].mean()
pros = opinions['pros'].count()
cons = opinions['cons'].count()
purchased = opinions['purchased'].sum()

#
stars_purchased = pd.crosstab(opinions['stars'], opinions['purchased'])

#
print(stars_avarage, pros, cons, purchased)
print(stars_purchased)