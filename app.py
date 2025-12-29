import os
from flask import Flask, render_template, request, redirect, url_for, flash
from data_manager import DataManager
from models import db, Movie

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'data/db.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
data_manager = DataManager()


@app.route('/')
def index():
    try:
        users = data_manager.get_users()
        return render_template('index.html', users=users)
    except Exception as e:
        print("Error loading users:", e)
        flash("An unexpected error occurred while loading users.", "error")
        return render_template('index.html', users=[])


@app.route("/users", methods=["POST"])
def create_user():
    try:
        name = request.form.get("name")
        if not name:
            flash("User name cannot be empty.", "error")
        else:
            data_manager.create_user(name)
            flash(f"User '{name}' created successfully.", "success")
    except Exception as e:
        print("Error creating user:", e)
        flash("An unexpected error occurred while creating the user.", "error")
    return redirect(url_for("index"))


@app.route('/users/<int:user_id>/movies')
def user_movies(user_id):
    try:
        user = data_manager.get_user_by_id(user_id)
        if not user:
            flash("User not found.", "error")
            return redirect(url_for("index"))

        movies = data_manager.get_user_favorites(user_id)
        return render_template("user_movies.html", user=user, movies=movies)

    except Exception as e:
        print(f"Error loading movies for user {user_id}:", e)
        flash("An unexpected error occurred while loading movies.", "error")
        return redirect(url_for("index"))


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_user_movie(user_id):
    try:
        title = request.form.get("title")
        if not title:
            flash("Movie title is required.", "error")
            return redirect(url_for('user_movies', user_id=user_id))

        movie = data_manager.create_movie(title)
        if not movie:
            flash(f"Movie '{title}' not found in OMDb.", "error")
            return redirect(url_for('user_movies', user_id=user_id))

        data_manager.add_favorite_movie(user_id, movie.id)
        flash(f"Movie '{movie.name}' added to favorites.", "success")
        return redirect(url_for('user_movies', user_id=user_id))

    except Exception as e:
        print(f"Error adding movie for user {user_id}:", e)
        flash("An unexpected error occurred while adding the movie.", "error")
        return redirect(url_for('user_movies', user_id=user_id))


@app.route('/movies/<int:movie_id>/update-title', methods=['POST'])
def update_movie_title(movie_id):
    try:
        new_title = request.form.get("title")
        if not new_title:
            flash("Title cannot be empty.", "error")
            return redirect(request.referrer)

        movie = Movie.query.get_or_404(movie_id)
        movie.name = new_title
        db.session.commit()
        flash("Movie title updated successfully.", "success")
        return redirect(request.referrer)

    except Exception as e:
        print(f"Error updating movie {movie_id}:", e)
        flash("An unexpected error occurred while updating the movie.", "error")
        return redirect(request.referrer)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_user_movie(user_id, movie_id):
    try:
        user = data_manager.remove_favorite_movie(user_id, movie_id)
        if user is None:
            flash("User or movie not found.", "error")
        else:
            flash("Movie removed from favorites.", "success")
        return redirect(url_for('user_movies', user_id=user_id))

    except Exception as e:
        print(f"Error deleting movie {movie_id} for user {user_id}:", e)
        flash("An unexpected error occurred while deleting the movie.", "error")
        return redirect(url_for('user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(400)
def bad_request(e):
    return render_template("400.html"), 400


if __name__ == '__main__':
  with app.app_context():
    db.create_all()

  app.run(debug=True, port=5002)
