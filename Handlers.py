import requests
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bs4 import BeautifulSoup
from ConfigBot import admin_id
from main import bot, dp
import feedparser

async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text="Для выбора категории новостей введите /new")

@dp.message_handler(Command("News"))
async def show_menu(message: Message):

    #По ссылке парсим все
    URL_YANDEX_NEWS = 'https://yandex.ru/news/export'
    r = requests.get(URL_YANDEX_NEWS)
    soup = BeautifulSoup(r.text, 'html.parser')

    #словарь будет хранить все URL(value) + text(key)
    allHref = {}

    #выбираем только ссылки
    for link in soup.find_all("a"):
         allHref[link.string] = link.get("href")

    #Из всех выбираем только те что для избранной рубрики
    #категории указаны в файле RubricText.txt
    favoriteСategories = []
    with open('RubricText.txt', 'r', encoding="utf-8") as f:
        favoriteСategories = f.read().splitlines()

    #словарь будет хранить только необходимые рубрики URL + text
    needLink = {}
    #перебираем все элементы списка и проверяем если такой ключ в словаре
    for item in favoriteСategories:
        if item in allHref:
            needLink[item] = allHref[item]

    #формируем кнопки
    buttonRubric = InlineKeyboardMarkup(row_width=2)
    for item in needLink:
        buttonRubric.insert(InlineKeyboardButton(text=item, callback_data=needLink[item]))

    await message.answer(text="Укажите рубрику", reply_markup=buttonRubric)

#---------------------События
@dp.callback_query_handler()
async def buying_pear(call: CallbackQuery):
    await call.answer(cache_time=5)

    #Парсим rss
    NewsFeed = feedparser.parse(call.data)

    iter = 0
    needLink = {}
    for item in NewsFeed['entries'][iter]:
        needLink[NewsFeed['entries'][iter]['title']] = NewsFeed['entries'][iter]['links'][0]['href']
        iter += 1

    #print(needLink)
    # формируем кнопки
    buttonRubric = InlineKeyboardMarkup(row_width=1)
    for item in needLink:
        buttonRubric.insert(InlineKeyboardButton(text=item, url=needLink[item]))

    await call.message.answer(text="Выбирите новость", reply_markup=buttonRubric)


