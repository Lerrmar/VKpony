import requests
from bs4 import BeautifulSoup


class Weather:
    @staticmethod
    def get_weather_today() -> list:
        http = "https://sinoptik.com.ru/погода-санкт-петербург"
        b = BeautifulSoup(requests.get(http).text, "html.parser")

        # result = ''
        # result = result + ('Утром :' + weather1) + '\n'
        # result = result + ('Днём :' + weather3 + ' ' + weather4) + '\n'
        temp = b.select('.weather__article_description-text')
        weather = temp[0].getText()

        url = 'https://yandex.ru/pogoda/2'
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        current_weather = soup.find('div', {'class': 'fact__time-yesterday-wrap'})
        current_weather_temperature = soup.find('div', {'class': 'temp fact__temp fact__temp_size_s'})
        current_weather_temperature1 = soup.find('div', {'class': 'term term_orient_h fact__feels-like'})
        result = current_weather.text + '\n' + current_weather_temperature.text + '\n' + current_weather_temperature1.text + '\n' + weather.strip()

        return result
#print(Weather.get_weather_today())