"""
Author: Isaac List
Date: May 27, 2021
"""

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Flask Application"""

from flask import Flask, session, redirect, url_for, escape, request, render_template, Response, jsonify
from config import app, db
from models import Book, BookSchema, User, UserSchema
import os
import json
import sys
import requests


app.secret_key = os.environ.get("SECRET_KEY")
app.google_key = os.environ.get("GOOGLE_KEY")


@app.route("/")
def index():
    if "username" in session:
        return render_template("index.html")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        return redirect(url_for("index"))

    # Add username to database if not there
    return render_template("login.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """Add a book to the book database"""
    cats: list = [
        "Fantasy",
        "Historical Fiction",
        "Science Fiction",
        "Contemporary",
        "Short Stories"
    ]

    if request.method == "GET":
        return render_template("add_book.html", categories = cats, alert = "")
    elif request.method == "POST":
        title: str = request.form.get("title")
        author: str = request.form.get("author")
        category: str = request.form.get("category")
        isbn: int = request.form.get("isbn")

        book = Book(
            title = title,
            author = author,
            category = category,
            isbn = isbn
        )

        db.session.add(book)
        db.session.commit()

        al: str = f"{title} by {author} added successfully"
        return render_template("add_book.html", categories = cats, alert = al)


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    """add a user to the user table"""
    if request.method == "GET":
        return render_template("add_user.html")
    elif request.method == "POST":
        username: str = request.form.get("name")
        userid: int = request.form.get("uid")

    user = User(
        username = username,
        userid = userid
    )

    db.session.add(user)
    db.session.commit()

    al: str = f"{username} added successfully"
    return render_template("add_user.html", alert = al)


@app.route("/list")
def list():
    """Display a list of the books in the database"""
    books = Book.query.all()
    book_schema = BookSchema(many=True)
    return render_template("list.html", items = book_schema.dump(books))


@app.route("/api/v1/books")
def api():
    """Access list of book titles and ISBN's in JSON format"""
    books = Book.query.all()
    book_schema = BookSchema(many=True)
    bookdata = book_schema.dump(books)

    resp: dict = {}
    for b in books:
        resp[b.title] = b.isbn

    resp_json: str = Response(json.dumps(resp))
    resp_json.headers["Access-Control-Allow-Origin"] = "*"
    resp_json.headers["Content-Type"] = "application/json"

    return resp_json


@app.route("/details", methods=["GET", "POST"])
def details():
    """Display book details using both local and Google Books APIs"""

    # Uses details.js to populate select menu with options from local API

    if request.method == "GET":
        return render_template("details.html", dets = "")

    elif request.method == "POST":
        try:
            isbn: str = request.form.get("sel_book")

            url: str = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn
            # Get url json
            book_request = requests.get(url)
            book_json = book_request.json()["items"][0]["volumeInfo"]
            book_details = {
                "title": book_json["title"],
                "author": book_json["authors"][0],
                "page_count": book_json["pageCount"],
                "pub_year": book_json["publishedDate"][:4],
                "description": book_json["description"]
            }

            return render_template("details.html", dets = book_details)

        except:
            err: str = "Book does not have a valid ISBN"
            return render_template("details.html", error = err)
            


@app.route("/logout")
def logout():
    """Logout the current session user"""
    session.pop("username", None)
    return redirect(url_for("index"))
