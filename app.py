from flask import Flask, jsonify, request

app = Flask(__name__)

# Local Array: data hanya tersimpan selama server berjalan
books = [
    {
        "id": 1,
        "title": "Laskar Pelangi",
        "author": "Andrea Hirata",
        "year": 2005
    },
    {
        "id": 2,
        "title": "Bumi",
        "author": "Tere Liye",
        "year": 2014
    }
]

next_id = 3


def find_book(book_id):
    return next((book for book in books if book["id"] == book_id), None)


def validate_book(data):
    if not isinstance(data, dict):
        return "Request body harus berupa JSON object."

    for field in ("title", "author", "year"):
        if field not in data:
            return f"Field '{field}' wajib diisi."

    if not isinstance(data["title"], str) or not data["title"].strip():
        return "Title harus berupa teks dan tidak boleh kosong."

    if not isinstance(data["author"], str) or not data["author"].strip():
        return "Author harus berupa teks dan tidak boleh kosong."

    # Tolak boolean dan teks untuk field year
    if type(data["year"]) is not int or data["year"] < 0:
        return "Year harus berupa bilangan bulat positif atau nol."

    return None


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "REST API Manajemen Buku berjalan",
        "endpoints": [
            "GET /books",
            "GET /books/<id>",
            "POST /books",
            "PUT /books/<id>",
            "DELETE /books/<id>"
        ]
    }), 200


@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books), 200


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = find_book(book_id)

    if book is None:
        return jsonify({"error": "Buku tidak ditemukan."}), 404

    return jsonify(book), 200


@app.route("/books", methods=["POST"])
def create_book():
    global next_id

    data = request.get_json(silent=True)
    error = validate_book(data)

    if error:
        return jsonify({"error": error}), 400

    book = {
        "id": next_id,
        "title": data["title"].strip(),
        "author": data["author"].strip(),
        "year": data["year"]
    }

    books.append(book)
    next_id += 1

    return jsonify({
        "message": "Buku berhasil ditambahkan.",
        "book": book
    }), 201


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = find_book(book_id)

    if book is None:
        return jsonify({"error": "Buku tidak ditemukan."}), 404

    data = request.get_json(silent=True)
    error = validate_book(data)

    if error:
        return jsonify({"error": error}), 400

    book["title"] = data["title"].strip()
    book["author"] = data["author"].strip()
    book["year"] = data["year"]

    return jsonify({
        "message": "Buku berhasil diperbarui.",
        "book": book
    }), 200


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = find_book(book_id)

    if book is None:
        return jsonify({"error": "Buku tidak ditemukan."}), 404

    books.remove(book)

    return jsonify({
        "message": "Buku berhasil dihapus.",
        "book": book
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
