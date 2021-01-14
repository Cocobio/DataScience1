import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url_str = "https://store.steampowered.com/search/"
tags_file = "tags.csv"
steam_data = 'table.csv'

headers = [	'Game title', 'Release date', 'Price', 'Discount price',
			'User review', 'Platform', 'Tag']
tags = pd.read_csv(tags_file)


####################################################################
					# WEB SCRAP FROM URL
####################################################################

# Set to True for web scrapping the data
# Data will be saved on a csv file, defined in steam_data
web_scrap = False

if web_scrap:
	data_dict = {h:[] for h in headers}

	for code, tag in zip(tags['Código'],tags['Etiqueta']):
		print(code, tag)
		steam = requests.get(url_str, params = { "specials": 1, "tags": str(code)+" # "+tag })
		soup = BeautifulSoup(steam.text, 'lxml')

		# If the search yields no games, then skip this iteration
		game_titles = [d.text for d in soup.find_all('span', attrs={'class':'title'})]
		if(len(game_titles)==0):
			continue

		data_dict[headers[0]] += game_titles
		data_dict[headers[1]] += [d.text for d in soup.find_all('div', attrs={'class':'search_released'})]

		normal_price = [float(''.join(filter(lambda x: x.isdigit(), '0' if d.text.find('$')==-1 else d.text.split('$')[1].strip()) ))      for d in soup.find_all('div', attrs={'class':'search_price'})]
		data_dict[headers[2]] += normal_price
	
		discount_price = [float('Nan' if not d.find('span') else '0' if d.text.split('$')[-1].strip().find('Free')!=-1 else ''.join(filter(lambda x: x.isdigit(), d.text.split('$')[-1].strip())))      for d in soup.find_all('div', attrs={'class':'search_price'})]
		data_dict[headers[3]] += discount_price
		
		data_dict[headers[4]] += [(0 if d.find('span',attrs={'mixed'}) else 1 if d.find('span',attrs={'positive'}) else -1 if d.find('span',attrs='negative') else float('Nan')) for d in soup.find_all('div',attrs={'search_reviewscore'})]
		
		# Vectorization of categorical data. 001 = bit for window support, 010 = bit for mac support, 100 = bit for linux support
		data_dict[headers[5]] += [((1 if d.find('span',attrs={'win'}) else 0) + (2 if d.find('span',attrs={'mac'}) else 0) + (4 if d.find('span',attrs={'linux'}) else 0)) for d in soup.find_all('p')]
		data_dict[headers[6]] += [tag for i in range(len(data_dict[headers[5]])-len(data_dict[headers[6]]))]

	# Create panda's DataFrame and save as csv
	steam_scrapped = pd.DataFrame(data_dict)
	steam_scrapped.to_csv(steam_data)


####################################################################
					# TABLE WORK
####################################################################
##### Exercise 1
# print('*'*70)
# print('\n\nExercise 1: Cheapest 10 games, excluding the ones that are already free')
steam_scrapped = pd.read_csv(steam_data)
# cheapest_10 = steam_scrapped.drop_duplicates(headers[0])
# filter_free = cheapest_10[headers[2]]>0

# cheapest_10 = cheapest_10[filter_free]
# cheapest_10.sort_values(headers[3], inplace=True)

# print(cheapest_10.head(10)[[headers[0],headers[2],headers[3]]])

# ##### Exercise 2
# win_mac_linux = steam_scrapped.drop_duplicates(headers[0])
# win_mac_linux = win_mac_linux[win_mac_linux[headers[5]]==7]

# print('*'*70)
# print('\n\nExercise 2: Games that work on windows, linux and mac')
# print(win_mac_linux[headers[0]])

# ##### Exercise 3
# discount_game_under_5k = steam_scrapped.drop_duplicates(headers[0])
# discount_game_under_5k = discount_game_under_5k[discount_game_under_5k[headers[3]]<=5000]

# game_value_under_15k = steam_scrapped.drop_duplicates(headers[0])
# game_value_under_15k = game_value_under_15k[game_value_under_15k[headers[2]]<=15000]


# print('*'*70)
# print('\n\nExercise 3: Games with discount value under $5.000')
# print(discount_game_under_5k[[headers[0],headers[3]]])
# print('\n',game_value_under_15k[[headers[0],headers[2]]])

# ##### Exercise 4
# avr_discount = steam_scrapped.drop_duplicates(headers[0])
# avr_discount = avr_discount[avr_discount[headers[3]]<avr_discount[headers[2]]]

# print('*'*70)
# print('\n\nExercise 4: Average value for games on discount:')
# print(avr_discount[headers[3]].mean())
# # print(avr_discount[[headers[0], headers[2],headers[3],headers[6]]])


# ##### Exercise 5
# games_per_platform_data = steam_scrapped.drop_duplicates(headers[0])
# games_per_platform_data = games_per_platform_data[headers[5]].value_counts()

# games_per_platform = pd.DataFrame({'Platform':['Windows','Windows & Mac', 'Windows & Linux', 'Windows, Mac & Linux', 'Unrecognized'], 'Count':games_per_platform_data[[1,3,5,7,0]]})

# print('*'*70)
# print('\n\nExercise 5: Games per platform:')
# print(games_per_platform)


# ##### Exercise 6
# print('*'*70)
# print('\n\nExercise 6: Cheapest games with discount per tag:')
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
# print(steam_scrapped.sort_values([headers[6],headers[3]]).drop_duplicates(headers[6]))



print(steam_scrapped[steam_scrapped[headers[2]]==0])