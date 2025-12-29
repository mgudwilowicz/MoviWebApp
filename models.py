from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorites = db.Table(
    "favorites",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("movie_id", db.Integer, db.ForeignKey("movie.id"), primary_key=True),
)


class User(db.Model):
    """User model representing a person with favorite movies."""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    favorite_movies = db.relationship(
        "Movie",
        secondary=favorites,
        back_populates="users"
    )

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"<User id={self.id} name='{self.name}'>"


class Movie(db.Model):
    """Movie model representing a movie that can be favorited by users."""

    __tablename__ = "movie"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    director = db.Column(db.String)
    year = db.Column(db.Integer)
    poster_url = db.Column(db.String)

    users = db.relationship(
        "User",
        secondary=favorites,
        back_populates="favorite_movies"
    )

    def __str__(self):
        return f"{self.name} ({self.year})"

    def __repr__(self):
        return f"<Movie id={self.id} title='{self.name}'>"
