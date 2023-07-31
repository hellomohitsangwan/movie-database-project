from flask import Flask
from routes.movies_routes import movie_routes
from routes.ratings_routes import rating_routes
from routes.users_routes import users_routes
from controllers.all_controllers import create_tables

app = Flask(__name__)

create_tables()
app.register_blueprint(movie_routes)
app.register_blueprint(users_routes)
app.register_blueprint(rating_routes)

if __name__ == '__main__':
    app.run(debug=True)
