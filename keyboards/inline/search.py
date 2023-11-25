from typing import Sequence

from aiogram.types import InlineKeyboardMarkup

from callback_data.paginator import PaginatorCallback
from database.movie_data import MovieData


def search_kb(
        movies: Sequence[MovieData],
        pg: PaginatorCallback = PaginatorCallback(),
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardMarkup()
    pg.add_pagination_buttons(builder, len(movies))
    return builder
