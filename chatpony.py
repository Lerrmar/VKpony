# -*- coding: utf-8 -*-
# Версия API: 5:100
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import random
import time
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import re
import dice
import confpo
import datetime
import traceback
import sys
import os


# полезные ссылки https://vk-api.readthedocs.io/en/latest/_modules/vk_api/bot_longpoll.html
# полезные ссылки https://vk.com/dev/messages.send
# полезные ссылки https://qna.habr.com/q/686454
# про парсинг https://fulyankin.github.io/Parsers/
def main():
    while True:  # цикл если вдруг бот где то навернется на пол пути то весь код перезапустится
        try:
            vk_session = vk_api.VkApi(token=confpo.token)  # ваш токен из группы, тут всё просто
            # print(vk_session)

            longpoll = VkBotLongPoll(vk_session, confpo.idsession)  # id вашей группы
            vk = vk_session.get_api()
            print(vk)
            for event in longpoll.listen():
                # print(longpoll)
                # print("longpoll")

                if event.type == VkBotEventType.MESSAGE_NEW:  # если нам написали сообщение
                    # print('Новое сообщение')  # для отслеживания работоспособности
                    # print(event)  # данные от сервера с которыми работает бот
                    dacepis = re.search(r'\d+d\d+', event.obj.text)

                    if event.obj.text == event.obj.text:  # если боту написали определенный текст
                        print("Новое сообщение - " + event.obj.text)
                        print(time.asctime(time.localtime(time.time())))
                        texta = ["Держи пони", "Лови", "Вот, наслаждайся", "Моё почтение(нет)"]
                        tagall = 4500
                        tag = "mlp+art/"
                        if re.search(r'\bВано\b', event.obj.text):
                            texta = ['Не шали', 'Приготовь огнетушитель', '18+', 'Руки на стол']
                            tagall = 260
                            tag = "eropony/"
                            print("Эро + " + event.obj.text)
                        elif re.search(r'\bкомикс\b', event.obj.text):
                            texta = ['Почитай', 'Годный комикс', 'Читать понравилось?', 'Ну хоть не эротика']
                            tagall = 396
                            tag = "mlp+комиксы/"
                            print("Комиксы " + event.obj.text)
                        elif re.search(r'\d+d\d+', event.obj.text):
                            daceplus = re.search(r'\+\d+', event.obj.text)
                            dacer = dice.roll(dacepis.group())
                            sumdace = sum(dacer)
                            print(dacepis.group())
                            print(dacer)
                            print(sumdace)
                            # print(daceplus.group(int()))
                            # print(bool(daceplus))
                            if re.search(r'\+\d+', event.obj.text):
                                sumdacemod = sumdace + int(daceplus.group())
                                vk.messages.send(
                                    peer_id=event.obj.peer_id,
                                    random_id=get_random_id(),
                                    message=("Держи кубы - " + dacepis.group() + '\n' + str(dacer) + ' Сумма ' + str(sumdace) + '\n' + 'Модификатор ' + str(daceplus.group()) + ' = ' + str(sumdacemod)),
                                )
                            else:
                                vk.messages.send(
                                    peer_id=event.obj.peer_id,
                                    random_id=get_random_id(),
                                    message=("Держи кубы - " + dacepis.group() + '\n' + str(dacer) + ' Сумма ' + str(sumdace)),
                                )

                            break

                        UserAgent().chrome  # маскировка под браузер, что бы бот на сайте не выглядел как бот

                        number = random.randrange(1, tagall)  # это если вдруг на сайте множество страниц
                        numsist = str(number)
                        print(number)
                        # Начало парсинга
                        main_pagest = 'http://mlp.reactor.cc/tag/' + tag + numsist  # для вашего сайта скорее всего придется изменить
                        main_page = str(main_pagest)
                        print(main_page)
                        response = requests.get(main_page)
                        html = response.content
                        soup = BeautifulSoup(response.text, "html.parser")
                        scans = soup.find_all("div", {"class": "image"})
                        # print(issues)
                        # print("issues " * 5)
                        obj23 = []  # про добавление в список https://coderoad.ru/15050756/%D0%9D%D0%B5%D0%B2%D0%BE%D0%B7%D0%BC%D0%BE%D0%B6%D0%BD%D0%BE-%D0%BD%D0%B0%D0%BF%D0%B5%D1%87%D0%B0%D1%82%D0%B0%D1%82%D1%8C-%D0%BE%D1%82%D0%B4%D0%B5%D0%BB%D1%8C%D0%BD%D1%83%D1%8E-%D1%81%D1%82%D1%80%D0%BE%D0%BA%D1%83-%D1%81-random-choice-%D1%82%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE-%D0%BE%D1%82%D0%B4%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5-%D1%81%D0%B8%D0%BC%D0%B2%D0%BE%D0%BB%D1%8B
                        for scan in scans:  # пробегаем по коду страницы и вычленяем ссылки
                            try:
                                obj2 = scan.find("a")["href"]
                            except:
                                pass
                            obj23.append(obj2)
                        itogpony = random.choice(obj23)  # рандомно выбираем ссылку, возможно вам и не нужно всё это
                        print(itogpony)
                        print("itogpony " * 5)
                        print()

                        url = [itogpony]  # парсится фото с сайта

                        def get_file(url):  # обычная загрузка изображения на комп
                            response = requests.get(url, stream=True)
                            return response

                        def save_data(name, file_data):
                            file = open(name, 'bw')  # Бинарный режим, изображение передається байтами
                            for chunk in file_data.iter_content(4096):  # Записываем в файл по блочно данные
                                file.write(chunk)

                        def get_name(url):
                            name = 'pony.jpg'
                            return name

                        for name in url:
                            save_data(get_name(name), get_file(name))
                        # time.sleep(1)

                        uploader = vk_api.upload.VkUpload(vk)  # обычная загрузка изображения в ВК
                        img = uploader.photo_messages("pony.jpg")
                        media_id = str(img[0]['id'])
                        owner_id = str(img[0]['owner_id'])

                        vk.messages.send(
                            peer_id=event.obj.peer_id,  # peer_id уникальное ид для чата, from_id ид того кто написал
                            random_id=get_random_id(),
                            message=(random.choice(texta)),
                            # message=("Держи пони - " + event.obj.text),
                            attachment=("photo" + owner_id + "_" + media_id)
                        )
                        # print(vk.messages.send)
                        # print("vk.messages.send")


                else:
                    # print(event.type)
                    # print("event.type")
                    print()


        except:
            if 'log.txt' in os.listdir():
                full = open('logfull.txt', 'w+')
                old = open ('log.txt', 'r')
                full.write(old.read())
                full.close()
                old.close()
            file = open('log.txt','w')
            file.write(str(datetime.datetime.now())+"\n")
            traceback.print_tb(sys.exc_info()[2], file=file)
            file.write(str(sys.exc_info()[1]))
            file.close()


if __name__ == '__main__':
    main()
