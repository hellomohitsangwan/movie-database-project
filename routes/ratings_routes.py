from flask import Blueprint, request, jsonify
import sqlite3
from controllers.all_controllers import *
# from auth.auth import token_required

rating_routes = Blueprint('rating_routes', __name__)

# Route to update the rating of a movie
@rating_routes.route('/update_rating', methods=['POST'])
@token_required
def update(current_user):
    data = request.get_json()

    movie_id = data.get('movie_id', None)
    rating = data.get('rating', None)

    if movie_id is None or rating is None:
        return jsonify({"message": "Movie ID and rating must be provided in the request data."}), 400

    # Validate the rating to be between 1 and 10 (you can customize this range)
    if not 1 <= rating <= 10:
        return jsonify({"message": "Invalid rating. Please provide a rating between 1 and 10."}), 400

    result = update_rating(current_user, movie_id, rating)

    if result[1] == 200:
        return jsonify({'token': result[0]['message']}), 200
    else:
        return jsonify({'message': result[0]['message']}), 401


# Route to get the average rating of each movie
@rating_routes.route('/average_rating', methods=['GET'])
def get_average_rating():
    # Get the average ratings of each movie
    success, result = get_average_ratings()

    if not success:
        return jsonify({"message": result}), 500

    return jsonify(result), 200
