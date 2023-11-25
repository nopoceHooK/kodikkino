import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from callback_data.paginator import PaginatorCallback
from config_data.config import API_KEY
from database.database import Movies
from database.movie_data import MovieData
from keyboards.inline.search import search_kb
from keyboards.inline.search_again import keyboard
from loader import dp, bot
from states.states import Search


@dp.message_handler(commands=['search'], state=None)
async def search_movie_command(message: types.Message):
    """
    Хендлер реагирующий на команду /search и получающий название фильма от пользователя
    """
    await bot.send_message(message.from_user.id, text="Введите название фильма для поиска: ")
    await Search.search_name.set()


@dp.message_handler(state=Search.search_name)
async def search_movies_list_by_name(message: types.Message, state: FSMContext):
    """
    Хендлер для поиска фильма по названию в базе кинопоиска
    """
    try:
        movie_name = message.text
        request = requests.get(f'https://api.kinopoisk.dev/v1.3/movie?name={movie_name}',
                               headers={'X-API-KEY': API_KEY})
        data = request.json()
        movies_list_data = data['docs']
        await message.answer(f'Найдено результатов: {len(movies_list_data)}')
        if movies_list_data:
            movies: list[MovieData] = []
            for movie_data in movies_list_data:
                movie = MovieData.from_dict(movie_data)
                movies.append(movie)
                Movies.save_search(message, movie, "search")

            await state.update_data(
                pg_consumer=search_kb,
                pg_data=movies,
            )

            paginator = PaginatorCallback(limit=1)
            movie = paginator.slice_first(movies)

            await message.answer_photo(
                movie.get_poster(),
                caption=movie.get_description(),
                reply_markup=search_kb(movies, paginator)
            )
            await state.set_state()
        else:
            await message.answer(f'Фильм {movie_name} не найден.')
            await state.finish()
        await message.answer(text='Не нашли что искали? Повторите поиск', reply_markup=keyboard)
    except Exception as e:
        await message.answer('Что-то пошло не так, попробуйте позже')


@dp.callback_query_handler(lambda c: c.data == 're_search', state=None)
async def process_callback_button(message: types.Message):
    """
    Хендлер для обработки кнопки повторного поиска
    """
    await bot.send_message(message.from_user.id, text="Введите название фильма для поиска: ")
    await Search.search_name.set()
