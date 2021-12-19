# Booklog
A book-journal type of project, developed as a
[Luther College](https://luther.edu) CS-330 Final Project.

## Project Overview
[More info to come later :D]

## Getting Started

### Python install and setup
To run this project, install Python (> 3.7) and create a new Virtual Environment:

`python3 -m venv venv`

Use pip to install the requirements, including [Flask](https://flask.palletsprojects.com/en/2.0.x/):

`python3 -m pip install -r requirements.txt`

### Setting Environment Variables
This project expects the following environment variables in a file `.env` in the
root of the project directory:
 - SECRET_KEY="ABC123" generated with [Secrets](https://docs.python.org/3/library/secrets.html)
 - GOOGLE_KEY=ABC123 found by registering for a
 [Google Books API Key](https://developers.google.com/books/docs/overview)
