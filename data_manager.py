from data_fetcher import fetch_movie
from models import db, User, Movie


class DataManager:
    """Class to manage users, movies, and favorites in the database."""

    def get_users(self):
        """Return a list of all users."""
        return User.query.all()


    def get_user_by_id(self, user_id):
        """Return a user by ID, or None if not found."""
        return User.query.get(user_id)


    def create_user(self, name):
        """Create a new user and return it."""
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        return user


    def delete_user(self, user_id):
        """Delete a user by ID. Return deleted user or None if not found."""
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        db.session.delete(user)
        db.session.commit()
        return user


    def get_movies(self):
        """Return a list of all movies."""
        return Movie.query.all()


    def get_movie_by_id(self, movie_id):
        """Return a movie by ID, or None if not found."""
        return Movie.query.get(movie_id)


    def create_movie(self, name):
        """Fetch movie info from OMDb, create it in DB, or return None if not found."""
        movie_data = fetch_movie(name)
        if not movie_data:
            return None

        movie = Movie(
            name=movie_data["name"],
            director=movie_data["director"],
            year=movie_data["year"],
            poster_url=movie_data["poster_url"],
        )
        db.session.add(movie)
        db.session.commit()
        return movie


    def update_movie(self, movie_id, name=None, director=None, year=None, poster_url=None):
        """Update movie fields if provided. Return updated movie or None if not found."""
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


    def add_favorite_movie(self, user_id, movie_id):
        """Add a movie to a user's favorites. Return user or None if user/movie not found."""
        user = self.get_user_by_id(user_id)
        movie = self.get_movie_by_id(movie_id)

        if not user or not movie:
            return None

        if movie not in user.favorite_movies:
            user.favorite_movies.append(movie)
            db.session.commit()

        return user


    def remove_favorite_movie(self, user_id, movie_id):
        """Remove a movie from a user's favorites. Return user or None if not found."""
        user = self.get_user_by_id(user_id)
        movie = self.get_movie_by_id(movie_id)

        if not user or not movie:
            return None

        if movie in user.favorite_movies:
            user.favorite_movies.remove(movie)
            db.session.commit()

        return user


    def get_user_favorites(self, user_id):
        """Return a list of a user's favorite movies, or None if user not found."""
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        return user.favorite_movies
