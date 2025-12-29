from data_fetcher import fetch_movie
from models import db, User, Movie

class DataManager:

    def get_users(self):
        return User.query.all()

    def get_user_by_id(self, user_id):
        return User.query.get(user_id)

    def create_user(self, name):
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        return user

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        db.session.delete(user)
        db.session.commit()
        return user

    # ---------- MOVIES ----------

    def get_movies(self):
        return Movie.query.all()

    def get_movie_by_id(self, movie_id):
        return Movie.query.get(movie_id)

    def create_movie(self, name):
        movie_data = fetch_movie(name)
        if not movie_data:
            return None

        movie = Movie(
            name=movie_data['name'],
            director=movie_data['director'],
            year=movie_data['year'],
            poster_url=movie_data['poster_url']
        )
        db.session.add(movie)
        db.session.commit()
        return movie

    def update_movie(self, movie_id, name=None, director=None, year=None, poster_url=None):
        movie = self.get_movie_by_id(movie_id)
        if not movie:
            return None

        if name is not None:
            movie.name = name
        if director is not None:
            movie.director = director
        if year is not None:
            movie.year = year
        if poster_url is not None:
            movie.poster_url = poster_url

        db.session.commit()
        return movie


    # ---------- FAVORITES (MANY-TO-MANY) ----------

    def add_favorite_movie(self, user_id, movie_id):
        user = self.get_user_by_id(user_id)
        movie = self.get_movie_by_id(movie_id)

        if not user or not movie:
            return None

        if movie not in user.favorite_movies:
            user.favorite_movies.append(movie)
            db.session.commit()

        return user

    def remove_favorite_movie(self, user_id, movie_id):
        user = self.get_user_by_id(user_id)
        movie = self.get_movie_by_id(movie_id)

        if not user or not movie:
            return None

        if movie in user.favorite_movies:
            user.favorite_movies.remove(movie)
            db.session.commit()

        return user

    def get_user_favorites(self, user_id):
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        return user.favorite_movies