from dataclasses import dataclass


@dataclass
class MovieData:
    name: str
    original_name: str
    year: int
    rating: float
    genres: list
    countries: list
    link: str
    description: str
    poster: str

    @classmethod
    def from_dict(cls, movie: dict):
        genres = []
        countries = []
        description = ''
        # poster = open('utils/misc/blank.jpg', 'rb')
        if movie['poster']:
            poster = movie['poster']['url']
        else:
            poster = None
        name = movie['name']
        original_name = movie['alternativeName']
        if original_name is None:
            original_name = ''
        else:
            original_name = ' / ' + str(movie['alternativeName'])
        year = movie['year']
        rating = round(movie['rating']['kp'], 1)
        if movie['genres']:
            genres = [genre['name'] for genre in movie['genres']]
        if movie['countries']:
            countries = [country['name'] for country in movie['countries']]
        if movie['description']:
            description = movie['description']
        link = f'https://www.kinopoisk.ru/film/{movie["id"]}'

        return cls(
            name=name,
            original_name=original_name,
            year=year,
            rating=rating,
            genres=genres,
            countries=countries,
            link=link,
            description=description,
            poster=poster
        )

    def get_poster(self):
        if self.poster:
            return self.poster
        else:
            return open('utils/misc/blank.jpg', 'rb')

    def get_description(self):
        return (
            f'{self.name}{self.original_name} ({self.year})\n'
            f'Рейтинг: {self.rating}/10⭐️\n'
            f'Жанры: {", ".join(self.genres)}\n'
            f'Страны: {", ".join(self.countries)}\n'
            f'\n{self.description[:350] + "..."}\n'
            f'\n{self.link}'
        )
