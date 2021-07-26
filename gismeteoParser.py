import requests
from bs4 import BeautifulSoup

HEADERS = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36', 'accept': '*/*'}
URL = "https://www.gismeteo.ru"
SEARCH_URL = "https://www.gismeteo.ru/search"

def get_response(url):
	r = requests.get(url, headers=HEADERS)
	return r


def get_link(city):
	response = get_response(SEARCH_URL+f'/{city}')
	content = response.text
	soup = BeautifulSoup(content, 'html.parser')
	link = soup.find(lambda tag: tag.name == "h2" and "Населённые пункты" in tag.text).find_next(class_="catalog_item").find_next()["href"]
	return(URL + link + "now/")


def get_content(r):
	soup = BeautifulSoup(r.text, 'html.parser')
	time = soup.find(class_='now__time').text

	temperature = soup.find('span', class_='unit unit_temperature_c').text

	real_feel = 'По ощущению ' + soup.find(class_='now__feel').find_next().text

	weather_type = soup.find(class_='now__desc').text

	now_info = soup.find(class_='now__info nowinfo')

	wind_nonformat = now_info.find(class_='nowinfo__item nowinfo__item_wind').text
	wind_list = list(wind_nonformat)
	wind = ''
	for i in wind_list:
		if i == 'м' or i == 'С' or i == 'Ю' or i == 'ш' or i == 'с' or i == 'з' or i == 'ю' or i == 'в':
			wind = wind + f' {i}'
		elif i == 'р':
			wind = wind + f'{i} '
		else:
			wind = wind + f'{i}'

	pressure = 'Давление: ' + now_info.find(class_='nowinfo__item nowinfo__item_pressure').find(class_='nowinfo__value').text + ' мм рт. ст.'

	humidity = 'Влажность: ' + now_info.find(class_='nowinfo__item nowinfo__item_humidity').find(class_='nowinfo__value').text + '%'

	gm_activity = 'Г/м активность: ' + now_info.find(class_='nowinfo__item nowinfo__item_gm').find(class_='nowinfo__value').text + ' балл(а) из 9'

	water = 'Вода: ' + now_info.find(class_='nowinfo__item nowinfo__item_water').find(class_='nowinfo__value').text

	return (f'***{time}***\n{temperature}\n{real_feel}\n{weather_type}\n{wind}\n{pressure}\n{humidity}\n{gm_activity}\n{water}')
	
	


def parse(city):
	response = get_response(get_link(city))
	if response.status_code == 200:
		res = get_content(response)
		return res
	else:
		return 'Что-то пошло не так!'

