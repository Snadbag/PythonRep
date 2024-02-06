from flask import Flask, Response, jsonify, request
import json

HOST = "0.0.0.0"
PORT = "8080"

app = Flask(__name__)

LIBRARY = [
	{"id": 0, "name": "Rozpravka", "author": "Steven King", "price": 20},
	{"id": 1, "name": "FRIdzka", "author": "Viliam Lendel", "price": 0},
	{"id": 2, "name": "Metaprogramovanie", "author": "Jan Janech", "price": 12}
]

@app.route('/')
def index():
	return "200 OK"

@app.route('/asdf')
def test():
	return "asdf"

@app.route('/library', methods=["GET"])
def getLibrary():
	output = ""

	for book in LIBRARY:
		output += "Nazov: {}, autor: {}, cena {}€<br />".format(book["name"], book["author"], book["price"])

	return output, 200

@app.route("/library", methods=["POST"])
def addToLibrary():
	newBook = request.json

	lastID = 0
	for book in LIBRARY:
		if book['id'] > lastID:
			lastID = book['id']

	newBook['id'] = lastID + 1
	LIBRARY.append(newBook)

	return jsonify(newBook), 201

@app.route("/library/del/<int:id>", methods=["DELETE"])
def delBook(id):
	for book in LIBRARY:
		if book['id'] == id:
			LIBRARY.remove(book)
			return jsonify(book), 200
	return jsonify({"error": "not found"}), 404 

# main
if __name__ == "__main__":
	app.run(HOST, PORT)