# -*- coding: utf-8 -*-
# Версия API: 5:100
import importlib
import random
import time
import requests
import re
import confpo
import datetime
import traceback
import sys
import os

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from vk_api import VkUpload
from bs4 import BeautifulSoup


session = requests.Session()
vk_session = vk_api.VkApi(token=confpo.token)  # ваш токен из группы, тут всё просто
upload = VkUpload(vk_session)


def main():
    while True:  # цикл если вдруг бот где то навернется на пол пути то весь код перезапустится
        try:
            longpoll = VkBotLongPoll(vk_session, confpo.idsession)  # id вашей группы
            vk = vk_session.get_api()
            print(vk)
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:  # если нам написали сообщение
                    # print('Новое сообщение')  # для отслеживания работоспособности
                    # print(event)  # данные от сервера с которыми работает бот

                    if event.obj.text == event.obj.text:  # если боту написали определенный текст
                        print("Новое сообщение - " + event.obj.text)
                        print(time.asctime(time.localtime(time.time())))
                        texta = ["Держи пони", "Лови", "Вот, наслаждайся", "Моё почтение(нет)"]
                        tagall = 4500
                        tag = "mlp+art/"
                        if re.search(r'\bhelp\b', event.obj.text):
                            texta = ['Ваша молитва услышана, передаю значение команд:\n'
                                     '- Без команды бот кидает просто рандомную поню из классического набора, как сейчас.\n'
                                     '- Команда "Вано" кидает случайную пони с тэгом "eropony".\n'
                                     '- Команда "комикс" кидает случайный комикс, тэг "mlp+комиксы".\n'
                                     '- Команда написанная "с уважением" кидает 5 случайных пони с тэгом "eropony"\n'
                                     'Всего вам хорошего и держитесь там']

                            print("help + " + event.obj.text)
                        elif re.search(r'\bВано\b', event.obj.text):
                            texta = ['Не шали', 'Приготовь огнетушитель', '18+', 'Руки на стол',
                                     'Не спускайте глаз с Вано']
                            tagall = 260
                            tag = "eropony/"
                            print("Эро + " + event.obj.text)
                        elif re.search(r'\bкомикс\b', event.obj.text):
                            texta = ['Почитай', 'Годный комикс', 'Читать понравилось?', 'Ну хоть не эротика']
                            tagall = 396
                            tag = "mlp+комиксы/"
                            print("Комиксы " + event.obj.text)
                        elif re.search(r'\bс уважением\b', event.obj.text):
                            texta = ['Не шали', 'Приготовь огнетушитель', '18+', 'Руки на стол',
                                     'Не спускайте глаз со всех']

                            with open('gotovoe.txt') as inp:
                                ponyfile = inp.readlines()

                            itogpony5 = random.sample(set(ponyfile), 5)
                            print(itogpony5)
                            print("Эро + " + event.obj.text)

                            vk.messages.send(
                                peer_id=event.obj.peer_id,
                                random_id=get_random_id(),
                                message=(random.choice(texta)),
                                attachment=itogpony5,
                            )
                            break

                        number = random.randrange(1, tagall)  # это если вдруг на сайте множество страниц
                        numsist = str(number)
                        print(number)
                        result = None
                        while result is None:
                            try:
                                # Начало парсинга
                                main_pagest = 'http://mlp.reactor.cc/tag/' + tag + numsist  # для вашего сайта скорее всего придется изменить
                                main_page = str(main_pagest)
                                print(main_page)
                                response = requests.get(main_page)
                                soup = BeautifulSoup(response.text, "html.parser")
                                scans = soup.find_all("div", {"class": "image"})
                                obj23 = []
                                for scan in scans:  # пробегаем по коду страницы и вычленяем ссылки
                                    try:
                                        obj2 = scan.find("a")["href"]
                                    except:
                                        pass
                                    obj23.append(obj2)

                                attachments = []
                                image_url = random.choice(obj23)

                                print(image_url)
                                print('image_url')
                                image = session.get(image_url, stream=True)
                                photo = upload.photo_messages(photos=image.raw)[0]
                                attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id'])
                                                   )
                                print(attachments)

                                vk.messages.send(
                                    peer_id=event.obj.peer_id,
                                    # peer_id уникальное ид для чата, from_id ид того кто написал
                                    random_id=get_random_id(),
                                    message=(random.choice(texta)),
                                    # message=("Держи пони - " + event.obj.text),
                                    attachment=','.join(attachments),
                                )

                                result = 1
                            except:
                                pass
                else:
                    # print(event.type)
                    # print("event.type")
                    print('Хде пысьма?')


        except:
            if 'log.txt' in os.listdir():
                full = open('logfull.txt', 'w+')
                old = open('log.txt', 'r')
                full.write(old.read())
                full.close()
                old.close()
            file = open('log.txt', 'w')
            file.write(str(datetime.datetime.now()) + "\n")
            traceback.print_tb(sys.exc_info()[2], file=file)
            file.write(str(sys.exc_info()[1]))
            file.close()


if __name__ == '__main__':
    main()
