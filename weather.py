import re
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

class Citata:
    @staticmethod
    def get_citata() -> list:
        http = "https://citaty.info/random/"
        b = BeautifulSoup(requests.get(http).text, "html.parser")

        temp = b.find('div', {'class': 'field-item even last'})
        return temp.text


def rohan(request):

    if re.search(r'\bГондор зовет на помощь\b', request):
        citations = ['И Рохан явится',
                     'И Рохан явится',
                     'И Рохан явится']

    elif re.search(r'\bжопа\b', request):
        citations = ['Рохан не говорит "жопа" пёс!', 'Пertertшитель', 'Эрэктус тебе в мармелад', 'Зубы на стол',
                 'Оглянись!']

    elif re.search(r'\b1111\b', request):
        citations = ['Рох22ит "жопа" пёс!', 'Пer222ель', 'Эрэкту222мармелад', 'Зу222 стол',
                     'Огw33сь!']
    else:
        citations = ["Рохан недоволен тобою."]



    return citations