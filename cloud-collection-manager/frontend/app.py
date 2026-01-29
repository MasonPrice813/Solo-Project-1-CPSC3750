from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "books.json"

def load_books():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_books(books):
    with open(DATA_FILE, "w") as f:
        json.dump(books, f, indent=2)

# ---- READ (with paging) ----
@app.route("/books")
def get_books():
    page = int(request.args.get("page", 1))
    page_size = 10

    books = load_books()
    start = (page - 1) * page_size
    end = start + page_size

    return jsonify({
        "total": len(books),
        "page": page,
        "books": books[start:end]
    })

# ---- CREATE ----
@app.route("/books", methods=["POST"])
def add_book():
    data = request.json

    if not data.get("title") or not data.get("author") or not str(data.get("year")).isdigit():
        return jsonify({"error": "Invalid data"}), 400

    books = load_books()
    new_id = max(b["id"] for b in books) + 1

    book = {
        "id": new_id,
        "title": data["title"],
        "author": data["author"],
        "year": int(data["year"])
    }

    books.append(book)
    save_books(books)

    return jsonify(book), 201

# ---- UPDATE ----
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.json
    books = load_books()

    for book in books:
        if book["id"] == book_id:
            book["title"] = data["title"]
            book["author"] = data["author"]
            book["year"] = int(data["year"])
            save_books(books)
            return jsonify(book)

    return jsonify({"error": "Book not found"}), 404

# ---- DELETE ----
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    books = load_books()
    books = [b for b in books if b["id"] != book_id]
    save_books(books)
    return jsonify({"success": True})

# ---- STATS ----
@app.route("/stats")
def stats():
    books = load_books()
    avg_year = sum(b["year"] for b in books) // len(books)

    return jsonify({
        "total": len(books),
        "average_year": avg_year
    })

if __name__ == "__main__":
    app.run()
