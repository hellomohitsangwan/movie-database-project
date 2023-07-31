from flask import Blueprint, request, jsonify
from controllers.all_controllers import *
# from auth.auth import token_required

users_routes = Blueprint('users_routes', __name__)

# Route to register a new user
@users_routes.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    result = create_user(username, password)

    if result[1] == 201:
        return jsonify({'message': 'User registered successfully!'}), 201
    else:
        return jsonify({'message': result[0]['message']}), 400

# Route to log in a user
@users_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    result = login_user(username, password)

    if result[1] == 200:
        return jsonify({'token': result[0]['token']}), 200
    else:
        return jsonify({'message': result[0]['message']}), 401
