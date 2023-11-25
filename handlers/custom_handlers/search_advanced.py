import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from callback_data.paginator import PaginatorCallback
from config_data.config import API_KEY
from database.database import Movies
from database.movie_data import MovieData
from keyboards.inline.adv_search_again import keyboard
from keyboards.inline.search import search_kb
from keyboards.reply.genres_btn import genres_kb
from loader import dp, bot
from states.states import SearchData


@dp.message_handler(commands=['adv_search'])
async def adv_search(message: types.Message):
    """
    Хендлер для обработки команды /adv_search и принимающий год выпуска фильма от пользователя
    """
    await SearchData.year.set()
    await message.answer('Введите год выхода фильма или интервал в формате 1991-1998:\n'
                         '(или введите * для того, чтобы пропустить ввод)')


@dp.message_handler(state=SearchData.year)
async def process_year(message: types.Message, state: FSMContext):
    """
    Хендлер приниающий от пользователя жанр фильма
    """
    async with state.proxy() as data:
        data['year'] = message.text
    await SearchData.next()
    await message.answer("Принято! Введите жанр фильма:\n"
                         "(или введите * для того, чтобы пропустить ввод)", reply_markup=genres_kb)


@dp.message_handler(state=SearchData.genre)
async def process_genre(message: types.Message, state: FSMContext):
    """
    Хендлер приниающий от пользователя страну производства фильма
    """
    async with state.proxy() as data:
        data['genre'] = message.text.lower()
    await SearchData.next()
    await message.answer("Хорошо, теперь введите страну производства фильма:\n"
                         "(или введите * для того, чтобы пропустить ввод)")


@dp.message_handler(state=SearchData.country)
async def process_country(message: types.Message, state: FSMContext):
    """
    Хендлер приниающий от пользователя название фильма
    """
    async with state.proxy() as data:
        data['country'] = message.text
    await SearchData.next()
    await message.answer("И наконец, введите название фильма:\n"
                         "(или введите * для того, чтобы пропустить ввод)")


@dp.message_handler(state=SearchData.name)
async def process_name(message: types.Message, state: FSMContext):
    """
    Хендлер осуществляющий поиск по заданным параметрам
    """
    try:
        async with state.proxy() as data:
            data['name'] = message.text
        await state.finish()

        search_data = {'year': data['year'],
                       'genre': data['genre'],
                       'country': data['country'],
                       'name': data['name']
                       }
        name = year = genre = country = ''
        if search_data['year'] != '*':
            year = f'&year={data["year"]}'
        if search_data['genre'] != '*':
            genre = f'&genres.name={data["genre"]}'
        if search_data['country'] != '*':
            country = f'&countries.name={data["country"]}'
        if search_data['name'] != '*':
            name = f'&name={data["name"]}'
        request = requests.get(f"https://api.kinopoisk.dev/v1.3/movie?page=1&limit=10{name}{year}{genre}{country}",
                               headers={'X-API-KEY': API_KEY})
        movies_data = request.json()
        movies_list_data = movies_data['docs']
        await message.answer(f'Найдено результатов: {len(movies_list_data)}')
        if movies_list_data:
            movies: list[MovieData] = []
            for movie_data in movies_list_data:
                movie = MovieData.from_dict(movie_data)
                movies.append(movie)
                Movies.save_search(message, movie, "adv_search")

            await state.update_data(
                pg_consumer=search_kb,
                pg_data=movies,
            )

            paginator = PaginatorCallback(limit=1, data="search")
            movie = paginator.slice_first(movies)

            await message.answer_photo(
                movie.get_poster(),
                caption=movie.get_description(),
                reply_markup=search_kb(movies, paginator)
            )
            await state.set_state()
        else:
            await state.finish()
        await message.answer(text='Не нашли что искали? Повторите поиск', reply_markup=keyboard)
    except:
        await message.answer('Что-то пошло не так, повторите попытку позже')


@dp.callback_query_handler(lambda c: c.data == 'adv_re_search', state=None)
async def process_callback_button(message: types.Message):
    """
    Хендлер обрабатывающий нажатие кнопки повторного поиска
    """
    await SearchData.year.set()
    await bot.send_message(message.from_user.id, 'Введите год выхода фильма или интервал в формате 1991-1998:\n'
                                                 '(или введите * для того, чтобы пропустить ввод)')
