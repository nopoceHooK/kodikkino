from peewee import SqliteDatabase, Model, CharField, IntegerField, ForeignKeyField

from database.movie_data import MovieData

db = SqliteDatabase("history.db")


class User(Model):
    user_id = IntegerField(primary_key=True)
    username = CharField()

    class Meta:
        database = db


class Movies(Model):
    user = ForeignKeyField(User, related_name='movies')
    link = CharField()
    movie_name = CharField()
    year = IntegerField()
    category = CharField()

    class Meta:
        database = db

    @classmethod
    def save_search(cls, message, movie: MovieData, category: str):
        try:
            user_id = message.from_user.id
            username = message.from_user.username
            try:
                user = User.create(user_id=user_id, username=username)
                Movies.create(user=user, link=movie.link, movie_name=movie.name, year=movie.year,
                              category=category)
            except:
                user = User.get(User.user_id == user_id)
                Movies.create(user=user, link=movie.link, movie_name=movie.name, year=movie.year,
                              category=category)
        except Exception as Ex:
            print(Ex)


User.create_table()
Movies.create_table()
