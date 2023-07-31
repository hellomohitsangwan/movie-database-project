# Movie Database API

The Movie Database API allows users to interact with the movie database. Users can register, log in, retrieve a list of movies, rate movies, and view the average rating of each movie.

## Table of Contents

1. [Introduction](#introduction)
2. [Authentication](#authentication)
3. [Base URL](#base-url)
4. [Endpoints](#endpoints)
   - [User Registration](#user-registration)
   - [User Login](#user-login)
   - [Retrieve Movies](#retrieve-movies)
   - [Rate Movie](#rate-movie)
   - [Average Rating](#average-rating)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [Example Usage](#example-usage)
8. [License](#license)

## Introduction

The Movie Database API allows users to access and manage movies in the database. It provides endpoints for user registration, authentication, retrieving movie information, rating movies, and viewing the average rating of each movie.

## Authentication

Most API endpoints, except for user registration and login, require authentication using JSON Web Tokens (JWT). To access these endpoints, you need to include the JWT in the `Authorization` header of the HTTP request. The JWT is obtained by logging in using valid user credentials.

## Base URL

The base URL for all API endpoints is: `http://localhost:5000/`

## Endpoints

### User Registration

Endpoint: `/register`
Method: `POST`
Description: Register a new user.

### User Login

Endpoint: `/login`
Method: `POST`
Description: Log in an existing user and obtain the access token.

### Retrieve Movies

Endpoint: `/movies`
Method: `GET`
Description: Retrieve a list of movies.
Authentication: Required

### Rate Movie

Endpoint: `/rate_movie`
Method: `POST`
Description: Rate a movie.
Authentication: Required

### Average Rating

Endpoint: `/average_rating`
Method: `GET`
Description: View the average rating of each movie.
Authentication: Not required

## Error Handling

If an error occurs in the API request, the response will include an error message with an appropriate status code. Please refer to the controller for specific error codes and their meanings.


## Example Usage

To retrieve movies, you can send a GET request to the `/movies` endpoint with the `Authorization` header containing the access token:

