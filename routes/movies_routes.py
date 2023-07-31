from flask import Blueprint, request, jsonify
import sqlite3
from controllers.all_controllers import *

movie_routes = Blueprint('movie_routes', __name__)

@movie_routes.route('/add_movie', methods=['POST'])
@token_required
def add_movie_to_user_list(current_user):
    data = request.get_json()
    movie_title = data.get('title')
    movie_genre = data.get('genre')

    if not movie_title or not movie_genre:
        return jsonify({'message': 'Movie title and genre are required!'}), 400

    # Add the movie to the user's list
    success, message = add_movie_to_list(current_user, movie_title, movie_genre)

    if not success:
        return jsonify({"message": message}), 500

    return jsonify({"message": message}), 201


@movie_routes.route('/movies', methods=['GET'])
@token_required
def get_user_movies(current_user):
    # Get the movies list for the current user
    response, status_code = get_movies_list(request, current_user)

    return jsonify(response), status_code
    

# Populate movies data from the API
@movie_routes.route('/populate_movies', methods=['GET'])
@token_required
def populate_movies(current_user):
    return add_movies_from_api()
