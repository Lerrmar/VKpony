import requests
from bs4 import BeautifulSoup


class Weather:
    @staticmethod
    def get_weather_today() -> list:
        http = "https://www.fontanka.ru/"
        b = BeautifulSoup(requests.get(http).text, "html.parser")

        #temp = b.select('.weather__article_description-text')
        #weather = temp[0].getText()

        temp = b.find('div', {'class': 'B1kh'})
        temp2 = b.find_all('li', {'class': 'B1ax'})

        # current_weather_temperature = temp.find('div', {'class': 'temp fact__temp fact__temp_size_s'})
        # current_weather_temperature1 = temp.find('div', {'class': 'term term_orient_h fact__feels-like'})
        # result = current_weather.text + '\n' + current_weather_temperature.text + '\n' + current_weather_temperature1.text + '\n' + weather.strip()

        return temp2

print(Weather.get_weather_today())