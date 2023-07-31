import sqlite3
import jwt
import datetime
from functools import wraps
import requests
from flask import request, jsonify


# SQLite database setup
def create_tables():
    try:
        conn = sqlite3.connect('blitz_movies.db') 
        cursor = conn.cursor()
        # Create the 'users' table
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT NOT NULL,
                           password TEXT NOT NULL,
                           movies TEXT DEFAULT '')''')

        # Create the 'movies' table
        cursor.execute('''CREATE TABLE IF NOT EXISTS movies
                          (id INTEGER PRIMARY KEY,
                           adult INTEGER,
                           title TEXT,
                           original_language TEXT,
                           original_title TEXT,
                           overview TEXT,
                           popularity REAL,
                           release_date TEXT,
                           cu INTEGER,
                           rated_by_users REAL,
                           current_avg REAL)''')

         # Create 'user_ratings' table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_ratings (
                user_id TEXT NOT NULL,
                movie_id INTEGER NOT NULL,
                PRIMARY KEY (user_id, movie_id),
                FOREIGN KEY (user_id) REFERENCES users (username),
                FOREIGN KEY (movie_id) REFERENCES movies (id)
            )
        ''')                             

        conn.commit()
        conn.close()
        print("Tables 'users' and 'movies' created successfully.")
    except Exception as e:
        print("Error creating tables:", e)




# Middleware/ decorator
# JWT token creation
def create_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, 'test_secret', algorithm='HS256')  # Replace with a secure secret key

# Check if the token is valid
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, 'test_secret', algorithms=['HS256'])  # Replace with the same secure secret key used for encoding
            current_user = data['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return func(current_user, *args, **kwargs)

    return decorated



# Controllers

# @desc    Populate movie from the moviedb API
# @route   GET /populate_movies
# @access  Public
def add_movies_from_api():
    api_url = "https://api.themoviedb.org/3/trending/all/day"
    api_key = "479b7ef692a41ad3a6942ad04e49e4b6" 

    # Make the API call
    response = requests.get(api_url, params={"api_key": api_key})
    if response.status_code == 200:
        data = response.json()
        movies_list = data.get("results", [])

        # Connect to the database
        conn = sqlite3.connect('blitz_movies.db')
        cursor = conn.cursor()

        # Loop through the movies in the API response and insert them into the database
        for movie in movies_list:
            adult = 0
            title = movie.get("title", "")
            original_language = movie.get("original_language", "")
            original_title = movie.get("original_title", "")
            overview = movie.get("overview", "")
            popularity = movie.get("popularity", 0.0)
            release_date = movie.get("release_date", "")

            # Insert movie data into the 'movies' table with default values for 'rated_by_users' and 'current_avg'
            cursor.execute('''INSERT INTO movies (adult, title, original_language, original_title, overview, popularity, release_date, rated_by_users, current_avg)
                              VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0)''',
                           (adult, title, original_language, original_title, overview, popularity, release_date))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        return {"message": "Movies added to the database successfully."}, 200
    else:
        return {"message": "Failed to fetch data from the API."}, 500


# @desc    Register a new user
# @route   POST /register
# @access  Public
def create_user(username, password):
    conn = sqlite3.connect('blitz_movies.db')
    cursor = conn.cursor()

    # Request Validation
    cursor.execute('SELECT id FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    if user:
        conn.close()
        return {"message": "Username already exists!"}, 400

    # Insert the new user into the database
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

    return {"message": "User registered successfully!"}, 201


# @desc    Login user
# @route   POST /login
# @access  Public
def login_user(username, password):
    conn = sqlite3.connect('blitz_movies.db')
    cursor = conn.cursor()

    # Retrieve the user from the database
    cursor.execute('SELECT id, password FROM users WHERE username=?', (username,))
    user = cursor.fetchone()

    if not user or user[1] != password:
        conn.close()
        return {"message": "Invalid credentials!"}, 401

    # Create a JWT token for the user
    token = create_token(user[0])

    conn.close()

    return {"token": token}, 200


# @desc    Add a movie to the user's list
# @route   POST /add_movie
# @access  Private
def add_movie_to_list(current_user, movie_title, movie_genre):
    try:
        conn = sqlite3.connect('blitz_movies.db')
        cursor = conn.cursor()

        # Retrieve the user's current movie list
        cursor.execute('SELECT movies FROM users WHERE id=?', (current_user,))
        current_movies = cursor.fetchone()[0]

        # Append the new movie to the list
        new_movie = f'{movie_title} ({movie_genre})'
        updated_movies = f'{current_movies}, {new_movie}' if current_movies else new_movie

        # Update the user's movie list in the database
        cursor.execute('UPDATE users SET movies=? WHERE id=?', (updated_movies, current_user))
        conn.commit()
        conn.close()

        return True, f'Movie "{movie_title}" added to your list!'

    except Exception as e:
        print("Error adding movie to list:", e)
        return False, "An error occurred while adding movie to list."


# @desc     Get movies list for a user
# @route   GET /movies
# @access  Private
def get_movies_list(request, current_user):
    # Get the access token from the request headers
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'message': 'Token is missing!'}), 401

    # Connect to the database
    conn = sqlite3.connect('blitz_movies.db')
    cursor = conn.cursor()

    # Fetch movies list for the user from the 'users' table
    cursor.execute("SELECT movies FROM users WHERE id=?", (current_user,))
    result = cursor.fetchone()

    # Close the database connection
    conn.close()

    if result:
        movies_list = result[0].split(',') if result[0] else []
        return {"movies": movies_list}, 200
    else:
        return {"message": "Movies not found."}, 404


# @desc    Update the rating of a movie
# @route   POST /update_rating
# @access  Private
def update_rating(current_user, movie_id, rating):
    # Validate the rating to be between 1 and 10 (you can customize this range)
    if not 1 <= rating <= 10:
        return {"message": "Invalid rating. Please provide a rating between 1 and 10."}, 400

    # Connect to the database
    conn = sqlite3.connect('blitz_movies.db')
    cursor = conn.cursor()

    # Check if the user has already rated the movie
    cursor.execute("SELECT COUNT(*) FROM user_ratings WHERE user_id=? AND movie_id=?", (current_user, movie_id))
    result = cursor.fetchone()

    if result and result[0] > 0:
        # Close the database connection
        conn.close()
        return {"message": "You have already rated this movie. Cannot rate again."}, 400

    # Fetch the current rated_by_users and current_avg for the movie
    cursor.execute("SELECT rated_by_users, current_avg FROM movies WHERE id=?", (movie_id,))
    result = cursor.fetchone()

    if result:
        rated_by_users, current_avg = result

        # Calculate the new current_avg after considering the new rating
        new_total_ratings = current_avg * rated_by_users + rating
        rated_by_users += 1
        new_current_avg = new_total_ratings / rated_by_users

        # Update the 'movies' table with the new values
        cursor.execute("UPDATE movies SET rated_by_users=?, current_avg=? WHERE id=?", (rated_by_users, new_current_avg, movie_id))
        
        # Add entry to user_ratings table
        cursor.execute("INSERT INTO user_ratings (user_id, movie_id) VALUES (?, ?)", (current_user, movie_id))
        
        conn.commit()
        conn.close()

        return {"message": "Rating updated successfully."}, 200
    else:

        conn.close()
        return {"message": "Movie not found."}, 404


# @desc    Get the average rating of each movie
# @route   GET /average_rating
# @access  Public
def get_average_ratings():
    try:
        conn = sqlite3.connect('blitz_movies.db')
        cursor = conn.cursor()

        # Fetch the movies along with their current_avg from the 'movies' table
        cursor.execute("SELECT id, title, current_avg FROM movies")
        movie_records = cursor.fetchall()

        conn.close()

        # Create a list to store the movie data with average rating
        movies_with_ratings = []

        for movie_record in movie_records:
            movie_id, title, current_avg = movie_record

            if current_avg is None:
                # If the movie has not been rated yet, set the average rating to "NA"
                average_rating = "NA"
            else:
                # If the movie has a rating, format the average rating to two decimal places
                average_rating = "{:.2f}".format(current_avg)

            # Add the movie data to the list
            movie_data = {
                "id": movie_id,
                "title": title,
                "average_rating": average_rating
            }
            movies_with_ratings.append(movie_data)

        return True, movies_with_ratings

    except Exception as e:
        print("Error fetching average ratings:", e)
        return False, "An error occurred while fetching average ratings."
