# Movie Database Project

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Testing](#testing)
- [Error Handling](#error-handling)
- [Performance Considerations](#performance-considerations)
- [Security](#security)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Movie Database Project is a backend application that allows users to register, log in, and interact with a database of movies. Users can view a list of movies, rate them, and view the average rating of each movie. The application collects movie data from an external API and stores it in the database.

## Features

- User registration and login with secure password hashing
- Authentication using JSON Web Tokens (JWT)
- API endpoints to retrieve and rate movies
- Open API to view the average rating of each movie
- Error handling for invalid requests
- Unit tests to ensure proper functionality

## Technologies Used

- Python
- Flask (Web Framework)
- SQLAlchemy (ORM)
- JWT (JSON Web Tokens) for Authentication
- SQLite (Database)
- Requests (HTTP Library)
- pytest (Testing Framework)

## Getting Started

To get the project up and running on your local machine, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/movie-database-project.git`
2. Navigate to the project directory: `cd movie-database-project`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Run the Flask development server: `python app.py`
5. The application should now be running at `http://localhost:5000/`

## API Documentation

The API endpoints and their usage are documented in the [API documentation](API_DOCS.md). It includes information on how to use each endpoint, the required parameters, and the expected responses.

## Database Schema

The database schema for this project consists of two main tables:

1. Users: Stores user information including the username and hashed password.
2. Movies: Stores movie information including the title, genre, and average rating.

## Testing

py have been implemented to verify the functionality of various components of the application. To run the tests, execute the following command:

```bash
python -m pytest


