import datetime
import random

from flask import Flask, render_template, redirect, url_for, request, flash, abort

import tmdb_client

app = Flask(__name__)
filtry = {"popular": "Popular", "top_rated": "Top Rated", "now_playing": "Now Playing", "upcoming": "Upcoming"}
app.secret_key = b'my-secret'
FAVORITES = set()


@app.route("/favorites/add", methods=['POST'])
def add_to_favorites():
    data = request.form
    movie_id = data.get('movie_id')
    movie_title = data.get('movie_title')
    if movie_id and movie_title:
        FAVORITES.add(movie_id)
        flash(f'Dodano film {movie_title} do ulubionych!')
    return redirect(url_for('homepage'))


@app.route("/favorites/")
def show_favorites():
    if FAVORITES:
        movies = []
        for movie_id in FAVORITES:
            movie_details = tmdb_client.get_single_movie(movie_id)
            movies.append(movie_details)
    else:
        movies = []
    return render_template("homepage.html", movies=movies, filtry=filtry)


@app.route('/')
def homepage():
    selected_list = request.args.get('list_type', "popular")
    if selected_list not in filtry:
        selected_list = 'popular'
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    return render_template("homepage.html", movies=movies, current_list=selected_list, filtry=filtry)


@app.route("/movie/<int:movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    if details.get("success") == False:
        abort(404)
    cast = tmdb_client.get_single_movie_cast(movie_id)
    movie_images = tmdb_client.get_movie_images(movie_id)
    if len(movie_images.get("backdrops")) > 0:
        selected_backdrop = random.choice(movie_images.get("backdrops"))
    else:
        selected_backdrop = ""

    return render_template("movie_details.html", movie=details, cast=cast, selected_backdrop=selected_backdrop)


@app.context_processor
def utility_processor():
    return {"tmdb_image_url": tmdb_client.get_poster_url}


@app.route('/search')
def search():
    search_query = request.args.get("q", "")
    if search_query:
        movies = tmdb_client.search(search_query=search_query)
    else:
        movies = []
    return render_template("search.html", movies=movies, search_query=search_query)


@app.route('/today')
def today():
    movies = tmdb_client.get_airing_today()
    today = datetime.date.today()
    return render_template("today.html", movies=movies, today=today)


if __name__ == '__main__':
    app.run(debug=True)
