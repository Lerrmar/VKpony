# Версия API: 5:124
import asyncio
import time
import random
import requests
from bs4 import BeautifulSoup


from vkwave.bots import (
    BaseEvent,
    TokenStorage,
    Dispatcher,
    BotLongpollExtension,
    DefaultRouter,
    GroupId,
    EventTypeFilter,
    PayloadFilter,
    CommandsFilter,
    Keyboard, PhotoUploader, create_api_session_aiohttp, TextContainsFilter, BotEvent,
)
from vkwave.client import AIOHTTPClient
from vkwave.api import BotSyncSingleToken, Token, API, APIOptionsRequestContext
from vkwave.longpoll.bot import BotLongpoll, BotLongpollData
from vkwave.types.bot_events import BotEventType

import confpo
import weather

# logging.basicConfig(level=logging.DEBUG)
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
            obj23 = []
            for scan in scans:  # пробегаем по коду страницы и вычленяем ссылки
                try:
                    obj2 = scan.find("a")["href"]
                except:
                    pass
                obj23.append('https:' + str(obj2))

            image_url = random.sample(set(obj23), amt)
            result = 1
        except:
            print('Ошибка парсинга')
            pass
    return image_url


@router.registrar.with_decorator(EventTypeFilter("message_new"), TextContainsFilter("help"))
async def kb_handler(event: BaseEvent):
    print('Сообщение' + time.asctime(time.localtime(time.time())) + '\n' + '-' * 50)
    print('help')
    hp = "Ваша молитва услышана, передаю значение команд:\n" \
         " - Без команды бот кидает просто рандомную поню из классического набора, как сейчас.\n" \
         " - Команда <няш> кидает случайную пони с тэгом <eropony>. \n" \
         " - Команда <комикс> кидает случайный комикс, тэг <mlp+комиксы>. \n" \
         " - Команда написанная <с уважением> кидает 5 случайных пони с тэгом <eropony> \n" \
         " - Команда <арт> кидает случайный арт.\n" \
         " - Команда <погода> показывает прогноз погоды в Питере на сегодня(в разработке, пишите если нужна).\n" \
         " - Команда <тырим> отправляет вас в мир увлекательного заимствования, напишите тырим_http://ссылку на сайт реактора/tag/_тег с конца ссылки/_номер страницы.\n" \
         " Всего вам хорошего и держитесь там"
    # kb = Keyboard(one_time=True)
    # kb.add_text_button(text="Вано", payload={"hello": "world"})
    await event.api_ctx.messages.send(
        peer_id=event.object.object.message.peer_id,
        message=hp,
        # keyboard=kb.get_keyboard(),
        random_id=0,
    )

@router.registrar.with_decorator(EventTypeFilter("message_new"), TextContainsFilter("Гондор зовет на помощь"))
async def handler(event: BaseEvent):
    print('Сообщение' + time.asctime(time.localtime(time.time())) + '\n' + '-' * 50)
    print('Гондор зовет на помощь')
    message_text = event.object.object.message.text  # текст сообщения
    texts = weather.rohan(message_text)  # вызываем функцию из файла
    image_rohan = ["https://sun9-43.userapi.com/impg/7MeCyb5AUMr5hofVJtQaVs9u8xVlzXJWq4TF0Q/-slpwzDaP6E.jpg?size=1280x594&quality=96&sign=4c432dae34c6dc2de9af496d92f91dd0&type=album"]

    async with create_api_session_aiohttp(confpo.token) as api:  # какая то магия
        uploader = PhotoUploader(api)  # что то загружает фото
        big_attachment = await uploader.get_attachments_from_links(
            peer_id=event.object.object.message.peer_id,
            #links=reactorsoup('http://arda.reactor.cc/', 'new/', 736, None),
            links=image_rohan,
        )
        await api.messages.send(
            peer_id=event.object.object.message.peer_id,
            message=(random.choice(texts)),  # рандомно выбирает текст
            attachment=big_attachment,
            random_id=0
        )

@router.registrar.with_decorator(EventTypeFilter("message_new"), TextContainsFilter("няш"))
async def handler(event: BaseEvent):
    print('Сообщение' + time.asctime(time.localtime(time.time())) + '\n' + '-' * 50)
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
@router.registrar.with_decorator(EventTypeFilter("message_new"), TextContainsFilter("тырим"))
async def handler(event: BaseEvent):
    print('Сообщение ' + time.asctime(time.localtime(time.time())) + '\n' + '-' * 50)
    print('Тырим')
    while True:
        try:
            texts = ['Воу воу воу', 'Годный парс', 'Это вообще законно?', 'Ну хоть не жопки']
            mess = event.object.object.message.text
            reactormess = mess.split()
            async with create_api_session_aiohttp(confpo.token) as api:
                uploader = PhotoUploader(api)
                big_attachment = await uploader.get_attachments_from_links(
                    peer_id=event.object.object.message.peer_id,
                    links=reactorsoup(str(reactormess[2]), str(reactormess[3]), None, int(reactormess[4])),
                )
                await api.messages.send(
                    peer_id=event.object.object.message.peer_id,
                    message=(random.choice(texts)),
                    attachment=big_attachment,
                    random_id=0
                )
                break
        except:
            await event.api_ctx.messages.send(
                peer_id=event.object.object.message.peer_id,
                message="ОШИБКАААА, пиши правильно \n http://ссылка тут твоя ссылка на реактор/ eropony/ 260",
                random_id=0,
            )
            break


@router.registrar.with_decorator(EventTypeFilter("message_new"), TextContainsFilter("с уважением"))
async def handler(event: BaseEvent):
    print('Сообщение ' + time.asctime(time.localtime(time.time())) + '\n' + '-' * 50)
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



# @router.registrar.with_decorator(TextContainsFilter("культуры"))
# async def kb_handler(event: BaseEvent):
#     texts = ['Это тебе на вечер', 'Культуры захотелось?', 'Что читаешь?', 'Ты друзь',
#              'чмоки', '&#128526;', '&#128686;', '&#127793;', '&#127770;', '&#10084;']
#     kb = Keyboard(one_time=True)
#     kb.add_text_button(text="комикс", payload={"hello": "world"})
#     await event.api_ctx.messages.send(
#         peer_id=event.object.object.message.peer_id,
#         message=(random.choice(texts)),
#         keyboard=kb.get_keyboard(),
#         random_id=0,
#     )


@router.registrar.with_decorator(EventTypeFilter("message_new"), TextContainsFilter("погода"))
async def handler(event: BaseEvent):
    print('Сообщение ' + time.asctime(time.localtime(time.time())) + '\n' + '-' * 50)
    print('Погодка')
    await event.api_ctx.messages.send(
        peer_id=event.object.object.message.peer_id,
        message=weather.Weather.get_weather_today(),
        random_id=0,
    )

@router.registrar.with_decorator(EventTypeFilter("message_new"))
async def handler(event: BotEvent):
    print('Сообщение ' + time.asctime(time.localtime(time.time())) + '\n' + '-' * 50)
    texts = ["Держи пони", "Лови", "Вот, наслаждайся", "Моё почтение(нет)"]
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
