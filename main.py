from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv, find_dotenv
import requests
import os

load_dotenv(find_dotenv())
bot = Bot(os.getenv('token_bot'))
dp = Dispatcher(bot)
headers = {"X-API-KEY": os.getenv('token_search')}

print('start')

@dp.message_handler(commands= ['start'])
async def start_command(messege: types.Message):
    await messege.answer('Привет! Я бот для поиска фильмов.')


@dp.message_handler(commands=['search'])
async def get_movies_by_name(message: types.Message, page = 1, limit = 1):
    words = message.text.split()
    if len(words) > 1:
        name = ' '.join(words[1:])

    try:
        response = requests.get(
            'https://api.kinopoisk.dev/v1.2/movie/search',
            params={
                "query": name,
                "limit": limit,
                "page": page,
            },
            headers=headers
        )
        movie = response.json().get('docs', [])
        movie = movie[0]
        servise_url = 'https://www.tvigle.ru/search/?q='
        servise_movie_name = movie['name'].split()
        servise_respons_name = '%20'.join(servise_movie_name)
        servise_respons = servise_url + servise_respons_name
        movie_info = f"Название: {movie['name']}.\nГод: {movie['year']}\nОписание: {movie['shortDescription']}.\nСмотреть на Tvigle: {servise_respons}"
        movie_photo_url = movie['poster']
    except:
        movie_info= 'Введите название фильма!'

    await message.answer_photo(movie_photo_url, caption=movie_info)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


executor.start_polling(dp, skip_updates=True)