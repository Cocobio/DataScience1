import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

url_str = "https://store.steampowered.com/search/"
tags_file = "tags.csv"

fields = ['Nombre del juego', 'Fecha de lanzamiento', 'Precio original', 'Precio en oferta',
		'Review de los usuarios', 'Plataformas', 'Etiqueta del juego']

tags = pd.read_csv(tags_file)


####################################################################
					# WEB SCRAP FROM URL
####################################################################

steam = requests.get(url_str)
soup = BeautifulSoup(steam.text, 'lxml')

data = soup.find_all('span', attrs={'class':'title'})
# print(data[0])

# print(rows[0].span)

# print([r.span.text for r in rows])

rows = soup.select('.search_result_row')
steam_scrapped = pd.DataFrame({'title':[r.span.text for r in rows]})

print(steam_scrapped)