# Версия API: 5:124 версия бота 1.1
import asyncio
import string
import time
import random
import requests
import g4f
from bs4 import BeautifulSoup

from vkwave.bots import (
    BaseEvent, TokenStorage, Dispatcher, BotLongpollExtension,
    DefaultRouter, GroupId, EventTypeFilter, PhotoUploader,
    create_api_session_aiohttp, TextContainsFilter, BotEvent,
)

from vkwave.client import AIOHTTPClient
from vkwave.api import BotSyncSingleToken, Token, API
from vkwave.longpoll.bot import BotLongpoll, BotLongpollData


import confpo
import weather

bot_token = Token(confpo.token)
gid = confpo.idsession
router = DefaultRouter()

def reactorsoup(sitepars, tag, pages, pagesmess, amt=1, ):
    st = 1
    result = None
    while result is None:
        try:
            if pages is None:
                number = pagesmess
            else:
                number = random.randrange(1, pages) # рандом диапазона
            # цикл от ошибки
            st += 1
            if st == 5:
                result = 1
            main_page = sitepars + tag + str(number)  # конструктор ссылки
            response = requests.get(str(main_page))
            soup = BeautifulSoup(response.text, "html.parser")
            scans = soup.find_all("div", {"class": "image"})
            list_links = []
            for scan in scans:  # пробегаем по коду страницы и вычленяем ссылки
                try:
                    found_images = scan.find("a")["href"]
                except:
                    pass
                list_links.append('https:' + str(found_images))

            image_url = random.sample(set(list_links), amt)
            result = 1
        except:
            print('Ошибка парсинга')
            pass

    return image_url


@router.registrar.with_decorator(EventTypeFilter("message_new"), TextContainsFilter("help"))
async def kb_handler(event: BaseEvent):
    print('Сообщение' + time.asctime(time.localtime(time.time())) + '\n' + '-' * 50)
    print(event.object.object.message.text)
    print('help')

    hp = "Ваша молитва услышана, передаю значение команд:\n" \
         " - Без команды бот кидает просто рандомную поню из классического набора, как сейчас.\n" \
         " - Команда <няш> кидает случайную пони с тэгом <eropony>. \n" \
         " - Команда <комикс> кидает случайный комикс, тэг <mlp+комиксы>. \n" \
         " - Команда написанная <с уважением> кидает 5 случайных пони с тэгом <eropony> \n" \
         " - Команда <арт> кидает случайный арт.\n" \
         " Всего вам хорошего и держитесь там"

    await event.api_ctx.messages.send(
        peer_id=event.object.object.message.peer_id,
        message=hp,
        random_id=0,
    )


def get_gpt(promt) -> list:
    response = g4f.ChatCompletion.create(
        model= g4f.models.gpt_35_turbo,
        messages=[{"role": "user", "content": promt}],
    )
    return response


@router.registrar.with_decorator(EventTypeFilter("message_new"), TextContainsFilter("няш"))
async def handler(event: BaseEvent):
    print('Сообщение' + time.asctime(time.localtime(time.time())) + '\n' + '-' * 50)
    print(event.object.object.message.text)
    print('няш')
    texts = ['Не шали', 'Приготовь огнетушитель', '18+', 'Руки на стол',
             'Не спускайте глаз с няш']

    async with create_api_session_aiohttp(confpo.token) as api:
        uploader = PhotoUploader(api)
        big_attachment = await uploader.get_attachments_from_links(
            peer_id=event.object.object.message.peer_id,
            links=reactorsoup('http://mlp.reactor.cc/tag/', 'eropony/', 340, None),
        )

        await api.messages.send(
            peer_id=event.object.object.message.peer_id,
            message=(random.choice(texts)),
            attachment=big_attachment,
            random_id=0
        )


@router.registrar.with_decorator(EventTypeFilter("message_new"), TextContainsFilter("арт"))
async def handler(event: BaseEvent):
    print('Сообщение' + time.asctime(time.localtime(time.time())) + '\n' + '-' * 50)
    print(event.object.object.message.text)
    print('Культуры')
    texts = ['Это тебе на вечер', 'Культуры захотелось?', 'Что читаешь?', 'Ты друзь',
             'чмоки', '&#128526;', '&#128686;', '&#127793;', '&#127770;', '&#10084;']
    async with create_api_session_aiohttp(confpo.token) as api:
        uploader = PhotoUploader(api)
        big_attachment = await uploader.get_attachments_from_links(
            peer_id=event.object.object.message.peer_id,
            links=reactorsoup('http://reactor.cc/tag/', 'art/', 10787, None),
        )

        await api.messages.send(
            peer_id=event.object.object.message.peer_id,
            message=(random.choice(texts)),
            attachment=big_attachment,
            random_id=0
        )


@router.registrar.with_decorator(EventTypeFilter("message_new"), TextContainsFilter("комикс"))
async def handler(event: BaseEvent):
    print('Сообщение' + time.asctime(time.localtime(time.time())) + '\n' + '-' * 50)
    print(event.object.object.message.text)
    print('Комикс')
    texts = ['Почитай', 'Годный комикс', 'Читать понравилось?', 'Ну хоть не эротика']

    async with create_api_session_aiohttp(confpo.token) as api:
        uploader = PhotoUploader(api)
        big_attachment = await uploader.get_attachments_from_links(
            peer_id=event.object.object.message.peer_id,
            links=reactorsoup('http://mlp.reactor.cc/tag/', 'mlp+комиксы/', 412, None),
        )
        await api.messages.send(
            peer_id=event.object.object.message.peer_id,
            message=(random.choice(texts)),
            attachment=big_attachment,
            random_id=0
        )

@router.registrar.with_decorator(EventTypeFilter("message_new"), TextContainsFilter("с уважением"))
async def handler(event: BaseEvent):
    print('Сообщение ' + time.asctime(time.localtime(time.time())) + '\n' + '-' * 50)
    print(event.object.object.message.text)
    print('С уважением начало')
    texts = ['Не шали', 'Приготовь огнетушитель', '18+', 'Руки на стол',
             'Не спускайте глаз со всех']

    async with create_api_session_aiohttp(confpo.token) as api:
        uploader = PhotoUploader(api)
        st = 1
        result = None

        while result is None:
            try:
                st += 1
                print('с уважением ' + str(st))
                if st == 5:
                    result = 1
                big_attachment = await uploader.get_attachments_from_links(
                    peer_id=event.object.object.message.peer_id,
                    links=reactorsoup('http://mlp.reactor.cc/tag/', 'eropony/', 340, None, amt=5))
                result = 1
            except:
                print('Ошибка загрузки')
                pass

        await api.messages.send(
            peer_id=event.object.object.message.peer_id,
            message=(random.choice(texts)),
            attachment=big_attachment,
            random_id=0
        )

@router.registrar.with_decorator(EventTypeFilter("message_new"))
async def handler(event: BotEvent):
    print('Сообщение ' + time.asctime(time.localtime(time.time())) + '\n' + '-' * 50)
    print(event.object.object.message.text)

    async with create_api_session_aiohttp(confpo.token) as api:
        uploader = PhotoUploader(api)
        big_attachment = await uploader.get_attachments_from_links(
            peer_id=event.object.object.message.peer_id,
            links=reactorsoup('http://mlp.reactor.cc/tag/', 'mlp+art/', 5184, None),
        )

        await api.messages.send(
            peer_id=event.object.object.message.peer_id,
            message=weather.Citata.get_citata(),
            attachment=big_attachment,
            random_id=0
        )



async def main():
    client = AIOHTTPClient()
    token = BotSyncSingleToken(bot_token)
    api_session = API(token, client)
    api = api_session.get_context()
    lp_data = BotLongpollData(gid)
    longpoll = BotLongpoll(api, lp_data)
    token_storage = TokenStorage[GroupId]()
    dp = Dispatcher(api_session, token_storage)
    lp_extension = BotLongpollExtension(dp, longpoll)

    dp.add_router(router)
    await dp.cache_potential_tokens()
    await lp_extension.start()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

