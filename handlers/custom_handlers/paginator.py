from __future__ import annotations

from typing import Sequence, Callable

from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaPhoto
from aiogram.utils import exceptions

from callback_data.paginator import PaginatorCallback, paginator_query
from database.movie_data import MovieData
from loader import dp

PgConsumer = Callable[[Sequence, PaginatorCallback], types.InlineKeyboardMarkup]
PgProducer = Callable[[Sequence, PaginatorCallback], str]


@dp.callback_query_handler(paginator_query.filter())
async def paginator(
        call: types.CallbackQuery,
        callback_data: dict,
        state: FSMContext
):
    callback_data.pop("@")
    data = await state.get_data()
    pg_data: Sequence = data.get("pg_data")
    pg_consumer: PgConsumer = data.get("pg_consumer")
    await state.update_data(pg=callback_data)
    paginator_cb = PaginatorCallback(**callback_data)
    try:
        if paginator_cb.data == "search":
            movie: MovieData = paginator_cb.slice_first(pg_data)
            await call.message.edit_media(
                InputMediaPhoto(
                    movie.get_poster(),
                    caption=movie.get_description(),
                ),
                reply_markup=pg_consumer(pg_data, paginator_cb)
            )

    except exceptions.MessageNotModified as e:
        await call.answer('Сортировка не изменена')
