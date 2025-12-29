import os

from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager

from models import db, Movie

app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'data/db.sqlite')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()


@app.route('/')
def home():
    return "Welcome to Marti MoviWeb App!"

@app.route('/users')
def list_users():
    users = data_manager.get_users()
    return render_template("users.html", users=users)

@app.route("/users", methods=["POST"])
def add_user():
    name = request.form.get("name")
    if name:
        data_manager.create_user(name)
    return redirect(url_for("home"))

@app.route('/users/<int:user_id>/movies')
def user_movies(user_id):
    user = data_manager.get_user_by_id(user_id)
    if not user:
        return "User not found", 404

    movies = data_manager.get_user_favorites(user_id)
    return render_template("user_movies.html", user=user, movies=movies)

@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_user_movie(user_id):
    title = request.form.get("title")

    if not title:
        return "Movie title is required", 400

    movie = data_manager.create_movie(title)
    if not movie:
        return "Movie not found in OMDb", 404

    data_manager.add_favorite_movie(user_id, movie.id)

    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/movies/<int:movie_id>/update-title', methods=['POST'])
def update_movie_title(movie_id):
    new_title = request.form.get("title")

    if not new_title:
        return "Title is required", 400

    movie = Movie.query.get_or_404(movie_id)
    movie.name = new_title

    db.session.commit()

    return redirect(request.referrer)

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_user_movie(user_id, movie_id):
    user = data_manager.remove_favorite_movie(user_id, movie_id)

    if user is None:
        return "User or movie not found", 404

    return redirect(url_for('user_movies', user_id=user_id))


if __name__ == '__main__':
  with app.app_context():
    db.create_all()

  app.run(debug=True, port=5002)
