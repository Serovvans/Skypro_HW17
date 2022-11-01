from flask import request
from flask_restx import Api, Resource
from create_app import app, db
from data_base_ans_serialize.db import Movie, Director, Genre
from data_base_ans_serialize.schemes import MovieSchema, DirectorSchema, GenreSchema


# Создаём API и пространства имён
api = Api(app)
movie_ns = api.namespace("movies")
director_ns = api.namespace("directors")
genre_ns = api.namespace("genres")

db.create_all()


# Готовим схемы для сериализации и десериализации
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


# CBV для фильмов
@movie_ns.route("/")
class MoviesView(Resource):
    def get(self):
        genre_id = request.values.get("genre_id", default=None)
        director_id = request.values.get("director_id", default=None)
        if director_id is not None and genre_id is not None:
            movies = db.session.query(Movie).filter(Movie.director_id == director_id and
                                                    Movie.genre_id == genre_id).all()
        elif director_id is not None:
            movies = db.session.query(Movie).filter(Movie.director_id == director_id).all()
        elif genre_id is not None:
            movies = db.session.query(Movie).filter(Movie.genre_id == genre_id).all()
        else:
            movies = Movie.query.all()
        return movies_schema.dumps(movies), 200

    def post(self):
        movie_json = request.json
        movie = Movie(**movie_json)
        with db.session.begin():
            db.session.add(movie)

        return "", 201


@movie_ns.route("/<int:pk>")
class MovieView(Resource):
    def get(self, pk: int):
        try:
            movie = db.session.query(Movie).get(pk)
        except Exception as e:
            return str(e), 404
        return movie_schema.dumps(movie), 200

    def put(self, pk: int):
        data = request.json
        try:
            movie = db.session.query(Movie).get(pk)
        except Exception as e:
            return str(e), 404
        movie.id = data.get("id")
        movie.title = data.get("title")
        movie.description = data.get("description")
        movie.trailer = data.get("trailer")
        movie.year = data.get("year")
        movie.rating = data.get("rating")
        movie.genre_id = data.get("genre_id")
        movie.director_id = data.get("director_id")

        db.session.add(movie)
        db.session.commit()
        return "", 204

    def delete(self, pk: int):
        try:
            movie = db.session.query(Movie).get(pk)
        except Exception as e:
            return str(e), 404
        db.session.delete(movie)
        db.session.commit()

        return "", 204


# CBV для режиссёров
@director_ns.route("/")
class DirectorsView(Resource):
    def get(self):
        directors = Director.query.all()
        return directors_schema.dumps(directors), 200

    def post(self):
        data = request.json
        new_director = Director(**data)

        with db.session.begin():
            db.session.add(new_director)

        return "", 201


@director_ns.route("/<int:pk>")
class DirectorView(Resource):
    def get(self, pk: int):
        try:
            director = db.session.query(Director).get(pk)
        except Exception as e:
            return str(e), 404
        return director_schema.dumps(director), 200

    def put(self, pk: int):
        data = request.json
        try:
            director = db.session.query(Director).get(pk)
        except Exception as e:
            return str(e), 404
        director.id = data.get("id")
        director.name = data.get("name")

        db.session.add(director)
        db.session.commit()
        return "", 204

    def delete(self, pk: int):
        try:
            director = db.session.query(Director).get(pk)
        except Exception as e:
            return str(e), 404
        db.session.delete(director)
        db.session.commit()

        return "", 204


# CBV для жанров
@genre_ns.route("/")
class GenresView(Resource):
    def get(self):
        genres = Genre.query.all()
        return genres_schema.dumps(genres), 200

    def post(self):
        data = request.json
        new_genre = Genre(**data)

        with db.session.begin():
            db.session.add(new_genre)

        return "", 201


@genre_ns.route("/<int:pk>")
class GenreView(Resource):
    def get(self, pk: int):
        try:
            genre = db.session.query(Genre).get(pk)
        except Exception as e:
            return str(e), 404
        return genre_schema.dumps(genre), 200

    def put(self, pk: int):
        data = request.json
        try:
            genre = db.session.query(Genre).get(pk)
        except Exception as e:
            return str(e), 404
        genre.id = data.get("id")
        genre.name = data.get("name")

        db.session.add(genre)
        db.session.commit()
        return "", 204

    def delete(self, pk: int):
        try:
            genre = db.session.query(Genre).get(pk)
        except Exception as e:
            return str(e), 404
        db.session.delete(genre)
        db.session.commit()

        return "", 204


if __name__ == '__main__':
    app.run(debug=True)
